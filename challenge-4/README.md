# Challenge 4: What's wrong?

We have a binary which was compiled for x86_64 Linux platform, therefore we need a stable and compatible runtime environment to be able to analyze this file. Because I am operating on an Apple ARM machine I decided to use Docker to investigate the binary.

## Dockerfile

When we want to use Docker we need to take care of a specific platform option for the base image. Thus we have to use followin FROM statement, where we force the platform to be linux/amd64. The statement is:

```sh
FROM --platform=linux/amd64 debian:stable-slim
```

Why Debian? Because we want to provide a standard runtime that is as compatible as possible.

We assign the workdir to /app and copy the blackbox file into it:

```sh
WORKDIR /app

COPY blackbox /app/
```

We need to make sure that we have the permission to execute the blackbox file and also we need to make sure that the built-in apt-get package manager is update to date to be able to install packaged we might need at a later point of time:

```sh
RUN chmod +x /app/blackbox
RUN apt-get update
```

## Build & run the container

As we now have a Dockerfile which will suite our needs to investigate the binary, we need to build it with

```sh
docker build -t blackbox .
```

where `blackbox` will be the name of our image.

To be able to interactivley execute commands inside the container we need to overwrite the entrypoint and start it like this:

```sh
docker run -it --entrypoint bash localhost/blackbox
```
After executing this command we will find ourselves inside the container in the /app directory. Now we can start investigating the problem with the binary.

## Investigation of blackbox binary

First things first we try to execute the binary with

```sh
./blackbox
```

which outputs `Ooooh, what's wrong?`. This is great because we have proofed the compatibility of the x86_64 architecture of this container with our arm platform.

A first very naive check would be to use the cat command on this binary. A more useable way of analyzing this binary would be to use some tools of the binutils package. 

First we need to install binutils via ap

```sh
apt install -y binutils
```

The binutils package contains a tool called `strings`. It can be used to search for readable strings in files, in this case our blackbox binary:

```sh
strings ./blackbox
```

The output is

```sh
/lib64/ld-linux-x86-64.so.2
libc.so.6
printf
__cxa_finalize
access
__libc_start_main
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
u+UH
[]A\A]A^A_
the_magic_filez.txt
Congrats! :)
Ooooh, what's wrong? :(
:*3$"
GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.8060
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
main.c
__FRAME_END__
__init_array_end
_DYNAMIC
__init_array_start
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
_ITM_deregisterTMCloneTable
_edata
printf@@GLIBC_2.2.5
__libc_start_main@@GLIBC_2.2.5
__data_start
__gmon_start__
__dso_handle
_IO_stdin_used
__libc_csu_init
__bss_start
main
access@@GLIBC_2.2.5
__TMC_END__
_ITM_registerTMCloneTable
__cxa_finalize@@GLIBC_2.2.5
.symtab
.strtab
.shstrtab
.interp
.note.gnu.property
.note.gnu.build-id
.note.ABI-tag
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.got
.plt.sec
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.dynamic
.data
.bss
.comment
```

The output is very interesting and we may interpret some things:

### Runtime environment

```sh
/lib64/ld-linux-x86-64.so.2
libc.so.6
GLIBC_2.2.5
```

The binary uses a default C Runtime and is dependent from libc.so.6 which is a shared external library. After searching the web for `ld-linux-x86-64.so.2` we get the information from https://www.baeldung.com/linux/dynamic-linker that the binary uses dynamic linking.

We are not a 100% percent sure yet but with the information we got the blackbox binary was very likely written in C.

### Functions

```sh
printf
access
```

There are two function names in the output of the strings command which grab out attention. The `printf` command is most probably used to print the messages like `Ooooh, what's wrong?` and `Congrats! :)` (as stated in the task description).

The `access` function is used to check access for files and paths during the runtime.

### Suspicious Strings

From the beginning there were two string which we already know:

- Ooooh, what's wrong? :(
- Congrats! :)

This is common english language and human readable. One is the result of a successful execute of blackbox and the other will be displayed when something is wrong, which is the case when running executing the binary.

But there is just another string in the result of the strings command where we should pay attention:

- the_magic_filez.txt

### Hypothesis

Now that we have some important information we can make a hypothesis:

"The blackbox binary was written in C and uses the access() command to check if there exists a file called the_magic_filez.txt"

### Verification

Now that we made our hypothesis we need to verify it by execution. First we need to create a file called `the_magic_filez.txt` which creates an empty file for us:

```sh
touch the_magic_filez.txt
```

Next we simply re-run the blackbox binary:

```sh
./blackbox
```

and tada we get `Congrats! :)``

We have proofed that our assumption was correct and that the blackbox binary needed a file called `the_magic_filez.txt` in its directory to output the success message.
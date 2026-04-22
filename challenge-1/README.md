# Challenge 1: Basic search

We will use tools which are already integrated in most, if not all common Linux operating systems. Our focus is on finding solutions which are simple, efficient and get the job done.

## Count all lines with 500 HTTP code.

Using `grep` with `-E` flag and some regular expression is a simple way to get all the HTTP/x.x 500 status codes. Afterwards we will count the lines with `wc -l`

```sh
count_lines_500=$(grep -E ' HTTP/[0-9].[0-9] 500 ' sample.log | wc -l)
```
Why don't we just use `grep -c`? Yes, it would work but as we have good habbits we will create more robust solutions which would also work with a different log file, so we will also take care of the "HTTP/x.x" part.

## Count all GET requests from yoko to /rrhh location and if it was successful (200).

If we take a look at the sample.log file we will notice that the server logs the information in a structed way - like columns in a table. Therefore we will be using `awk` to grab the fields of interest and match them against our desired contents. In the end we count the lines of the result from awk.

```sh
count_get_yoko_rrhh=$(awk '$2=="yoko" && $5=="200" && $6=="\"GET" && $7=="/rrhh\""' sample.log | wc -l)
```

## How many requests go to /?

In this case we will use `awk` as it fits perfectly to check the 7th field of the log output for "/".

```sh
count_requests_root=$(awk '$7=="/\""' sample.log | wc -l)
```

## Count all lines without 5XX HTTP code.

This one is similar to the first task except that we filter all HTTP status codes beginning with "5" and invert the result of the `grep` command with the `-v` flag.

```sh
count_lines_without_5xx=$(grep -Ev ' HTTP/[0-9].[0-9] 5[0-9][0-9] ' sample.log | wc -l)
```

## Replace all 503 HTTP codes by 500, how many requests have a 500 HTTP code?

Note. As I have understood the replacement needs to be permanent, thus the changes must be saved persisted in the sample.log file.

`sed` is a great tool to accomplish the task. With the streamline editor we can comfortably search for specific patterns and replace parts of them. In this case we don't need the `/g` because the status codes only appear once per line. In this case we use the `-E` flag which allows us to take regular expressions into account. `/\1500` is the critical part where `\1...` reuses the part defined in the brackets before.

There is just a little pitfall when using different os platforms where the command is run on (see comment in code). Thus we will use a little workaround by saving the result of `sed` in a temporary file and replace the original sample.log with it. 

```sh
sed -E 's/(HTTP\/[0-9.]+ )503 /\1500 /' sample.log > sample_temp.log
mv sample_temp.log sample.log
```
# cdrsnr
###### Dependencies : Python 2.7
###### By Matt Rienzo
###### Heavily based on Single_Number_Reporter source by Redemption.Man
###### Original repo: https://github.com/MWarren1/CUCM-Single-Number-Report


TODO:
- Update README.md
- Write output as CSV or XLSX based on -o or -a file extension

Changelog:
* Changed phone numbers to a regex so you can match patterns and lists
* Added an exclusion argument, using regex again
* Added an inclusion-as-forwarding argument, again with regex
* Added the ability to append to a file
* Added an output file argument to name the output path

```
usage: cdrsnr [-h] -i INPUT -n PHONENUMBER [-o OUTPUT] [-x EXCLUDE]
              [-l LIST_FORWARDED] [-a APPEND]

Reads Cisco CDR files and creates a simplfied call record for a single number

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        CDR file input (must be csv)
  -n PHONENUMBER, --phonenumber PHONENUMBER
                        Phone number regex to report on (remember to add 9 if
                        external number)
  -o OUTPUT, --output OUTPUT
                        Output file
  -x EXCLUDE, --exclude EXCLUDE
                        Excluded number regex pattern
  -l LIST_FORWARDED, --list-forwarded LIST_FORWARDED
                        List number regex as forwarded to number
  -a APPEND, --append APPEND
                        File to append records to
```

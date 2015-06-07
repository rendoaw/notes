for junos, it will remove  the whole interface em0 section (multiline) from config file
```
perl -ni -e 'print unless /^    em0 {/ .. /^    }/' *.conf
```
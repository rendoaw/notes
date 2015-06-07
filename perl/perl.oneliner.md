for junos, it will remove  the whole interface em0 section (multiline) from config file
```
perl -ni -e 'print unless /^    em0 {/ .. /^    }/' *.conf
```

print all lines except if contains specific string
```
perl -i -nle 'print if !/SECRET/' * 
```

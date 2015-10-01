

# Android #

## Similarities/Differences of applications (aka rip-off indicator) ##

**You will find all information and algorithms in the following [paper](http://www.phrack.org/issues.html?issue=68&id=15#article) (section 3)**

**For Windows, change "androsim.py" with "androsim.exe" :)**

### Androsim ###

This tool detects and reports:
  * the identical methods;
  * the similar methods;
  * the deleted methods;
  * the new methods;
  * the skipped methods.

Moreover, a similarity score (between 0.0 to 100.0) is calculated upon the values of the identical methods (1.0) and the similar methods (in this particular case, we calculate the final values using the BZ2 compressor due to the fact that the return value is more "interesting" for the score). It is more interesting because you will have an understandable value related to the similarity.

Ok, imagine that you have you have an Android application, and you have seen suspicious apps in the wild. You would like to have a real proof that the code of your application has been [ripped](http://www.net-security.org/secworld.php?id=11989), right ?


The first step is to get [Androguard](http://code.google.com/p/androguard/wiki/Installation) to use "androsim.py" or a binary [version](http://code.google.com/p/androguard/downloads/list).

After that you need to give two parameters on the command line:
```
desnos@t0t0:~/androguard$ ./androsim.py -i apks/plagiarism/htchen/dailymoney/dailymoney-0.9.5.apk apks/plagiarism/htchen/dailymoney/com.htc.dailymoney.apk 
Elements:
         IDENTICAL:     871
         SIMILAR:       96
         NEW:           228
         DELETED:       54
         SKIPPED:       0
        --> methods: 80.258346% of similarities
```

and you have your rip-off score !


You can specify with the option "-n" if you wish to have a final value only by getting information about the first app, and to don't care about the second app:
```
desnos@t0t0:~/androguard$ ./androsim.py -i apks/plagiarism/htchen/dailymoney/dailymoney-0.9.5.apk apks/plagiarism/htchen/dailymoney/com.htc.dailymoney.apk -n
Elements:
         IDENTICAL:     871
         SIMILAR:       96
         NEW:           228
         DELETED:       54
         SKIPPED:       0
        --> methods: 93.936066% of similarities
```

On windows:

![http://androguard.googlecode.com/files/1.2-7.png](http://androguard.googlecode.com/files/1.2-7.png)

#### Options ####

**-i**: specify the inputs

**usage**:
  * -i FILENAME FILENAME
  * -i FILENAME DIRECTORY

**-t**: specify the threshold (0.0 to 1.0) to know if a method is similar. This option will impact on the filtering method. Because if you specify a higher value of the threshold, you will have more associations.

**usage**:
  * -t 0.1
  * -t 0.4

**-c**: specify the compressor (BZ2, ZLIB, SNAPPY, LZMA, XZ). The final result depends directly of the type of compressor. But if you use LZMA for example, the final result will be better, but it take more time.

**usage**:
  * -c BZ2
  * -c SNAPPY

**-d**: display all methods names

**-n**: calculate the final score only by using the ratio of included methods

**-e**: specify which class you would like to force to exclude (skipped methods) (python regexp pattern)

**usage**:
  * -e "(Lorg/myclass1/)"
  * -e "(Lorg/myclass1/)|(Lorg/myclass2)"

**-s**: specify the minimum size of a method to be used (it is the length (bytes) of the dalvik method)

**usage**:
  * -s 10
  * -s 100

**-l**: use the python module for compression or specify another path for the native similarity library

**usage**:
  * -l python ---> force to use python module
  * -l mylibsimilarity.so

#### Examples ####

For the first test we use the "opfake" malware (http://code.google.com/p/androguard/wiki/DatabaseAndroidMalwares#opfake_(all)). If we take two samples from the same family, an important value of similarity is revealed:
```
#########################################################################
d@t0t0:~/androguard$ ./androsim.py -i apks/malwares/opfake/b79106465173490e07512aa6a182b5da558ad2d4f6fae038101796b534628311
apks/malwares/opfake/b906279e8c79a12e5a10feafe5db850024dd75e955e9c2f9f82bbca10e0585a6

Elements:
        IDENTICAL:     34
        SIMILAR:        5
        NEW:            0
        DELETED:        0
        SKIPPED:        0
       --> methods: 99.100500% of similarities
#########################################################################
```

These two samples have similar methods and it's possible to have more
information by specifying the "-d" option:
```
#########################################################################
SIMILAR methods:
       Lcom/reg/MainRegActivity; displayFakeProgress ()V 61
               --> Lcom/reg/MainRegActivity; displayFakeProgress ()V
                   61 0.0909090936184
       Lcom/reg/MainRegActivity; getNextButton ()Landroid/widget/Button;
       40
               --> Lcom/reg/MainRegActivity; getNextButton
               ()Landroid/widget/Button; 40 0.125
       Lcom/reg/MainRegActivity; showLinkForm ()V 111
               --> Lcom/reg/MainRegActivity; showLinkForm ()V
               111 0.183673471212
       Lcom/reg/MainRegActivity; showRules ()V 132
               --> Lcom/reg/MainRegActivity; showRules ()V
               132 0.0731707289815
       Lcom/reg/MainRegActivity; setMainScreen ()V 147
               --> Lcom/reg/MainRegActivity; setMainScreen ()V
               147 0.319148927927
IDENTICAL methods:
       Lcom/reg/MainRegActivity; PushMsg (Ljava/lang/String;
       Ljava/lang/String;)V 76
               --> Lcom/reg/MainRegActivity; PushMsg (Ljava/lang/String;
               Ljava/lang/String;)V 76

       Lcom/reg/SmsReceiver; setListener (Lcom/reg/SMSAction;)V 3
               --> Lcom/reg/SmsReceiver; setListener
               (Lcom/reg/SMSAction;)V 3

       Lcom/reg/MainRegActivity; loadString (I)Ljava/lang/String; 52
               --> Lcom/reg/MainRegActivity; loadString (I)
               Ljava/lang/String; 52

       Lcom/reg/MainRegActivity; access$600 ()Ljava/lang/String; 3
               --> Lcom/reg/MainRegActivity; access$600
               ()Ljava/lang/String; 3

       Lcom/reg/ParseXml; getXMLTags (Ljava/lang/String;
       Ljava/lang/String;)Ljava/util/Vector; 82
               --> Lcom/reg/ParseXml; getXMLTags (Ljava/lang/String;
               Ljava/lang/String;)Ljava/util/Vector; 82

       Lcom/reg/ParseXml; getXMLExtra (Ljava/lang/String;
       Ljava/lang/String;)Ljava/lang/String; 52
               --> Lcom/reg/ParseXml; getXMLExtra (Ljava/lang/String;
               Ljava/lang/String;)Ljava/lang/String; 52

       Lcom/reg/MainRegActivity; SaveSuccess ()V 23
               --> Lcom/reg/MainRegActivity; SaveSuccess ()V 23

       Lcom/reg/SmsReceiver; onReceive (Landroid/content/Context;
       Landroid/content/Intent;)V 59
               --> Lcom/reg/SmsReceiver; onReceive
               (Landroid/content/Context; Landroid/content/Intent;)V 59

       Lcom/reg/ParseXml; getXMLIntElement (Ljava/lang/String;
       Ljava/lang/String;)I 55
               --> Lcom/reg/ParseXml; getXMLIntElement
               (Ljava/lang/String; Ljava/lang/String;)I 55

       Lcom/reg/MainRegActivity; getCountry ()Ljava/lang/String; 13
               --> Lcom/reg/MainRegActivity; getCountry
               ()Ljava/lang/String; 13

       Lcom/reg/MainRegActivity$5; onReceive (Landroid/content/Context;
       Landroid/content/Intent;)V 35
               --> Lcom/reg/MainRegActivity$5; onReceive
               (Landroid/content/Context; Landroid/content/Intent;)V 35

       Lcom/reg/MainRegActivity$1; (Lcom/reg/MainRegActivity;)V 6
               --> Lcom/reg/MainRegActivity$1;
               (Lcom/reg/MainRegActivity;)V 6

       Lcom/reg/MainRegActivity$S_itm; (Lcom/reg/MainRegActivity;)V 21
               --> Lcom/reg/MainRegActivity$S_itm;
               (Lcom/reg/MainRegActivity;)V 21
[...]
NEW methods:
DELETED methods:
SKIPPED methods:
#########################################################################
```

Basically we are able to determine if two samples are from the same malware family. If they are, the analyst can start his analysis from the similar methods.

In the next part we will see how we can see the differences (what
instructions have been modified) between two similar methods. If we test
the tool by using two different samples (like opfake and foncy) we observe
the following:
```
#########################################################################
d@t0t0:~/androguard$ ./androsim.py -i apks/malwares/opfake/b79106465173490e07512aa6a182b5da558ad2d4f6fae038101796b534628311
apks/malwares/foncy/01f6f6379543f4aaa0d6b8dcd682f4e2b106527584b3645eb674f1646faccad5

Elements:
        IDENTICAL:     1
        SIMILAR:       0
        NEW:           2
        DELETED:       38
        SKIPPED:       0
       --> methods: 33.333333% of similarities
#########################################################################
```

We see a strange similarity score due to the fact that all methods,
including those of small size, have been compared. We can skip the specific
case of methods having a small size using the "-s" option (to filter
according to the size of the method in bytes):
```
#########################################################################
d@t0t0:~/androguard$ ./androsim.py -i
apks/malwares/opfake/b79106465173490e07512aa6a182b5da558ad2d4f6fae038101796b534628311
apks/malwares/foncy/01f6f6379543f4aaa0d6b8dcd682f4e2b106527584b3645eb674f1646faccad5 -s 10

Elements:
        IDENTICAL:     0
        SIMILAR:       0
        NEW:           2
        DELETED:       29
        SKIPPED:       33
       --> methods: 0.000000% of similarities
#########################################################################
```

We can do a lot of things with this kind of tool such as:
  * detecting plagiarism between two android applications
  * checking if an application is correctly protected with an obfuscator
  * extracting easily injected codes (if you know the original application)

There are many other interesting "ways" to use this tool such as
discovering if malware samples have been written by the same author, or if some pieces of code have been reused. Analyzing the "faketoken" (http://code.google.com/p/androguard/wiki/DatabaseAndroidMalwares#faketoken) sample and the "opfake.d" sample we have observed an interesting result.

The first sample "faketoken" is detected by 19/43 antivirus products on
VirusTotal (https://www.virustotal.com/file/f7c36355c706fc9dd8954c096825e0613807e0da4bd7f3de97de0aec0be23b79/analysis/). The second sample "opfake.d" is detected by 16/41 antivirus products on VirusTotal (https://www.virustotal.com/file/61da462a03d8651a6088958b438b44527973601e604e3ca18cb7aa0b3952d2ac/analysis/). All of these antivirus products are using different names  with the exception of DrWeb.

Now if we run our tool we observe the following output:
```
#########################################################################
d@t0t0:~/androguard$ ./androsim.py -i
apks/plagiarism/opfake/f7c36355c706fc9dd8954c096825e0613807e0da4bd7f3de97de0aec0be23b79
apks/plagiarism/opfake/61da462a03d8651a6088958b438b44527973601e604e3ca18cb7aa0b3952d2ac

Elements:
        IDENTICAL:     951
        SIMILAR:       5
        NEW:           34
        DELETED:       23
        SKIPPED:       0
       --> methods: 96.516954% of similarities
#########################################################################
```

We can skip specific libraries common to these samples such as
"Lorg/simpleframework/xml" and methods of small sizes. This provides us
with an even more interesting result:

```
#########################################################################
d@t0t0:~/androguard$ ./androsim.py -i
apks/plagiarism/opfake/f7c36355c706fc9dd8954c096825e0613807e0da4bd7f3de97de0aec0be23b79
apks/plagiarism/opfake/61da462a03d8651a6088958b438b44527973601e604e3ca18cb7aa0b3952d2ac
-e "Lorg/simpleframework/" -s 100 -d

Elements:
        IDENTICAL:     9
        SIMILAR:       3
        NEW:           14
        DELETED:       11
        SKIPPED:       5260
       --> methods: 44.998713% of similarities

SIMILAR methods:
       Ltoken/bot/MainApplication; loadStartSettings
       (Ljava/lang/String;)Ltoken/bot/StartSettings; 230
               --> Lcom/load/wap/MainApplication; loadStartSettings
               (Ljava/lang/String;)Lcom/load/wap/StartSettings; 190 0.375

       Ltoken/bot/MainService; threadOperationRun
       (I Ljava/lang/Object;)V 197
               --> Lcom/load/wap/MainService; threadOperationRun
               (I Ljava/lang/Object;)V 122 0.319999992847

       Ltoken/bot/ServerResponse; ()V 133
               --> Lcom/load/wap/ServerResponse; ()V 125 0.214285716414

IDENTICAL methods:
       Ltoken/bot/Settings; isDeleteMessage (Ljava/lang/String;
       Ljava/lang/String;)Z 132
               --> Lcom/load/wap/Settings; isDeleteMessage
               (Ljava/lang/String; Ljava/lang/String;)Z 132

       Ltoken/bot/UpdateActivity; setMainScreen ()V 107
               --> Lcom/load/wap/UpdateActivity; setMainScreen ()V 107

       Ltoken/bot/MainApplication; sendGetRequest (Ljava/lang/String;
       Ljava/util/List;)V 132
               --> Lcom/load/wap/MainApplication; sendGetRequest
               (Ljava/lang/String; Ljava/util/List;)V 132

       Ltoken/bot/MainService; onStart (Landroid/content/Intent; I)V 106
               --> Lcom/load/wap/MainService; onStart
               (Landroid/content/Intent; I)V 106

       Ltoken/bot/MainApplication; sendPostRequest (Ljava/lang/String;
       Ljava/util/List;)V 197
               --> Lcom/load/wap/MainApplication; sendPostRequest
               (Ljava/lang/String; Ljava/util/List;)V 197

       Ltoken/bot/MainApplication; DownloadApk (Ljava/lang/String;
       Ljava/lang/String;)Z 106
               --> Lcom/load/wap/MainApplication; DownloadApk
               (Ljava/lang/String; Ljava/lang/String;)Z 106

       Ltoken/bot/Settings; isCatchMessage (Ljava/lang/String;
       Ljava/lang/String;)Ltoken/bot/CatchResult; 165
               --> Lcom/load/wap/Settings; isCatchMessage
               (Ljava/lang/String; Ljava/lang/String;)
               Lcom/load/wap/CatchResult; 165

       Ltoken/bot/MainApplication; getContacts
       (Landroid/content/Context;)Ljava/util/Vector; 230
               --> Lcom/load/wap/MainApplication; getContacts
               (Landroid/content/Context;)Ljava/util/Vector; 230

       Ltoken/bot/MainApplication; dateFromString
       (Ljava/lang/String;)Ljava/util/Date; 103
               --> Lcom/load/wap/MainApplication; dateFromString
               (Ljava/lang/String;)Ljava/util/Date; 103
#########################################################################
```

As we can see, the names of the methods are "exactly" the same, and the
signatures (the bytecodes with a high probability) are the same. It can be really interesting to detect if your software has been ripped off by
someone.

### Androdiff ###

Now, we have a new tool called "androdiff.py" which can be used to extract
and observe differences between two Android applications. We have tested it
against two versions of the Skype application to analyze the patch of a
security vulnerability (http://www.androidpolice.com/2011/04/14/exclusive-vulnerability-in-skype-for-android-is-exposing-your-name-phone-number-chat-logs-and-a-lot-more/) (mainly due to incorrect use of file permissions):
```
#########################################################################
d@t0t0:~/androguard$ ./androsim.py -i
elsim/examples/android/com.skype.raider_1.0.0.831.apk
elsim/examples/android/com.skype.raider_1.0.0.983.apk -c BZ2

Elements:
        IDENTICAL:     2059
        SIMILAR:       167
        NEW:           27
        DELETED:       0
        SKIPPED:       0
       --> methods: 98.192539% of similarities
#########################################################################
```

We have several methods to analyze, but only a few new methods are present,
and two of them are particularly interesting:
```
#########################################################################
       Lcom/skype/ipc/SkypeKitRunner; chmod (Ljava/io/File;
                Ljava/lang/String;)Z 61
       Lcom/skype/ipc/SkypeKitRunner; fixPermissions ([Ljava/io/File;)V 47
#########################################################################
```

So we can now search in the similar methods where these new methods are
called:
```
#########################################################################
d@t0t0:~/androguard$ ./androdiff.py -i
elsim/examples/android/com.skype.raider_1.0.0.831.apk
elsim/examples/android/com.skype.raider_1.0.0.983.apk -d
[...]
[ ('Lcom/skype/ipc/SkypeKitRunner;', 'run', '()V') ] <->
[ ('Lcom/skype/ipc/SkypeKitRunner;', 'run', '()V') ]
run-BB@0xae run-BB@0xae
Added Elements(2)
        0xba 3 invoke-virtual v8 , [ meth@ 5897
        Ljava/security/MessageDigest; reset ['()', 'V'] ]
        0xc0 4 sget-object v9 , [ field@ 1299
        Lcom/skype/ipc/SkypeKitRunner; [B MAITSEAINE ]
Deleted Elements(0)

run-BB@0x320 run-BB@0x316
Added Elements(1)
        0x332 5 const/4 v8 , [ #+ 0 ] // {0}
Deleted Elements(1)
        0x328 5 const/4 v8 , [ #+ 3 ] // {3}

run-BB@0x352 run-BB@0x348
Added Elements(1)
        0x364 4 const-string v5 , [ string@ 2921 'chmod 750 ' ]
Deleted Elements(1)
        0x35a 4 const-string v5 , [ string@ 2904 'chmod 777 ' ]

run-BB@0x52c run-BB@0x522
Added Elements(10)
        0x59e 29 invoke-virtual v4 , [ meth@ 109
        Landroid/content/Context; getFilesDir ['()', 'Ljava/io/File;'] ]
        0x5a4 30 move-result-object v4
        0x5a6 31 invoke-virtual v4 , [ meth@ 5719
                 Ljava/io/File; getAbsolutePath ['()',
                 'Ljava/lang/String;'] ]
        0x5ac 32 move-result-object v4
        0x5be 37 move-object/from16 v0 , v19
        0x5c2 38 iget-object v0 , v0 , [ field@ 1314
                 Lcom/skype/ipc/SkypeKitRunner;
                 Landroid/content/Context; mContext ]
        0x5c6 39 move-object v4 , v0
        0x5d8 44 move-object/from16 v0 , v19
        0x5dc 45 move-object v1 , v4
        0x5de 46 invoke-direct v0 , v1 , [ meth@ 1923
                 Lcom/skype/ipc/SkypeKitRunner; fixPermissions
                 ['([Ljava/io/File;)', 'V'] ]
Deleted Elements(0)
[...]
#########################################################################
```

As you can see, some constants are changed (3 to 0, 777 to 750) to patch an
incorrect use of file permissions (you need to take the original CFG to
view the details (maybe in a new version we will see the results in one
CFG)). A new method is called to fix the existing permissions of the files.


## Add your application in a database: search quickly if your app has been rip-off ##

### Androsign ###

This tool can verify if a signature in the database matches with the input android application (DEX/APK).

```
desnos@destiny:~/androguard$ ./androsign.py -h
Usage: androsign.py [options]

Options:
  -h, --help            show this help message and exit
  -i INPUT, --input=INPUT
                        file : use this filename
  -d DIRECTORY, --directory=DIRECTORY
                        directory : use this directory
  -b DATABASE, --database=DATABASE
                        database : use this database
  -c CONFIG, --config=CONFIG
                        use this configuration
  -v, --verbose         display debug information
```

To test if an application is in the database :
```
desnos@destiny:~/androguard$ ./androsign.py -i apks/malwares/DroidDream/Magic\ Hypnotic\ Spiral.apk -b signatures/dbandroguard -c signatures/dbconfig 
Magic Hypnotic Spiral.apk : ----> DroidDream

desnos@destiny:~/androguard$ ./androsign.py -i apks/com.skype.raider_1.0.0.983.apk -b signatures/dbandroguard -c signatures/dbconfig 
com.skype.raider_1.0.0.983.apk : ----> None
```

or to test an entire directory :
```
desnos@destiny:~/androguard$ ./androsign.py -d apks/mixe/ -b signatures/dbandroguard -c signatures/dbconfig
594ebcc14a163b86222bd09adfe95498da81ceaeb772b706339d0a24858b1267 : ----> GoldDream
d615dd181124ca0fde3d4785786586c3593a61d2c25c567ff93b230eb6d3a97a : ----> DroidDreamLight
c6eb43f2b7071bbfe893fc78419286c3cb7c83ce56517bd281db5e7478caf995 : ----> Wat
com.rovio.angrybirdsseasons-1.apk : ----> None
c1a94e9fd0a6bda7e5ead89d8ef9ee064aeccdaf65238bf604f33e987a8656b9 : ----> DogoWar
add10b0368753ec38de0dca15550d824ac141f0c86f2f123f30551bd82e82415 : ----> DroidDream-Included
137274dccff625eb1f9d647b09ed50cdfa8f86fe1a893d951f1f04e0d91f85bc : ----> DroidDream
03fbe528af4e8d17aef4b8db67f96f2905a7f52e0342826aeb3ec21b16dfc283 : ----> DroidKungfu2
76e91e1f9cc3422c333e51b65bb98dd50d00f1f45a15d2008807b06c125e651a : ----> NickySpy
c687e2f0b4992bd368df0c24b76943c99ac3eb9e4e8c13422ebf1a872a06070a : ----> Geinimi
zimperlich.apk : ----> None
cf9ebba0501079d61cff24d00e2de662c591039d8ff7f0c982e2e2778d6cf49b : ----> NickySpy
7513c6a11b88b87f528b88624d1b198b5bcc325864b328e32cc0d790b0bfc1c4 : ----> DroidKungfu
```

You can specify the verbose option to have more information :
```
desnos@destiny:~/androguard$ ./androsign.py -d apks/mixe/ -b signatures/dbandroguard -c signatures/dbconfig -v
DroidKungfu (0)
        ---> METHSIM L:0 I:0 N:0 J:1 [4.8512959480285645, 4.6483860015869141, 4.6914162635803223, 4.7337584495544434, 4.2597851753234863]
NickySpy (0 or 1)
        ---> METHSIM L:1 I:1 N:0 J:2 [4.9857087135314941, 4.7834396362304688, 4.8159637451171875, 4.5245232582092285, 0.0]
        ---> METHSIM L:1 I:2 N:1 J:2 [4.9697809219360352, 4.7652387619018555, 4.8861689567565918, 4.5666427612304688, 4.2081961631774902]
DroidDreamLight (0)
        ---> METHSIM L:2 I:3 N:0 J:1 [4.7545814514160156, 4.6544718742370605, 3.8625667095184326, 4.5037317276000977, 0.0]
DroidKungfu2 (0 and 1)
        ---> METHSIM L:3 I:4 N:0 J:2 [4.3921775817871094, 4.0211343765258789, 4.5443987846374512, 4.1571140289306641, 3.9754178524017334]
        ---> METHSIM L:3 I:5 N:1 J:2 [4.5738983154296875, 4.3132176399230957, 4.6949276924133301, 4.4872374534606934, 4.0113649368286133]
Geinimi (0 or 1 or (2 and 3))
        ---> METHSIM L:4 I:6 N:0 J:4 [4.8281669616699219, 4.5770049095153809, 4.4555692672729492, 4.6577677726745605, 3.9754178524017334]
        ---> METHSIM L:4 I:7 N:1 J:4 [4.973602294921875, 4.7980365753173828, 4.5259051322937012, 4.5926632881164551, 4.1278433799743652]
        ---> METHSIM L:4 I:8 N:2 J:4 [3.2040255069732666, 1.4406454563140869, 4.5679025650024414, 4.5526924133300781, 3.9754178524017334]
        ---> METHSIM L:4 I:9 N:3 J:4 [4.6186771392822266, 4.4623689651489258, 1.6163301467895508, 4.5717849731445312, 0.0]
DogoWar (0 and 1)
        ---> CLASSSIM L:5 I:10 N:0 J:2 [4.5144822597503662, 4.3906300067901611, 2.7473165988922119, 3.9876822233200073, 0.0]
        ---> CLASSSIM L:5 I:11 N:1 J:2 [4.1654442787170414, 3.6046688079833986, 1.4984882354736329, 3.9250543117523193, 0.0]
Wat (0)
        ---> CLASSSIM L:6 I:12 N:0 J:1 [3.8983065400804793, 2.8835478850773404, 2.3970618758882796, 4.0557840211050848, 0.6026742117745536]
GoldDream (0 and 1)
        ---> METHSIM L:7 I:13 N:0 J:2 [4.9010534286499023, 4.7493586540222168, 4.5943202972412109, 4.6015524864196777, 0.0]
        ---> METHSIM L:7 I:14 N:1 J:2 [2.3710076808929443, 1.3113172054290771, 4.8033995628356934, 4.538449764251709, 3.9754178524017334]
DroidDream-Included (0)
        ---> METHSIM L:8 I:15 N:0 J:1 [4.9024319648742676, 4.7362179756164551, 4.5589680671691895, 4.422579288482666, 0.0]
DroidDream (0)
        ---> METHSIM L:9 I:16 N:0 J:1 [4.7122836112976074, 4.4915299415588379, 4.9674844741821289, 4.9468302726745605, 0.0]

594ebcc14a163b86222bd09adfe95498da81ceaeb772b706339d0a24858b1267 : loading apk.. loading dex.. check ... C:10 CC:4 CMP:87 EL:96 C:3 CC:1 CMP:12 EL:11 ----> GoldDream [[13, 0.13768115639686584], [14, 0.022988505661487579]]
d615dd181124ca0fde3d4785786586c3593a61d2c25c567ff93b230eb6d3a97a : loading apk.. loading dex.. check ... C:30 CC:4 CMP:410 EL:890 C:13 CC:3 CMP:41 EL:171 ----> DroidDreamLight [[3, 0.1629464328289032]]
c6eb43f2b7071bbfe893fc78419286c3cb7c83ce56517bd281db5e7478caf995 : loading apk.. loading dex.. check ... C:7 CC:5 CMP:49 EL:37 C:4 CC:2 CMP:3 EL:14 ----> Wat [[12, 0.11543287336826324]]
com.rovio.angrybirdsseasons-1.apk : loading apk.. loading dex.. check ... C:30 CC:4 CMP:785 EL:912 C:12 CC:2 CMP:26 EL:153 ----> None []
c1a94e9fd0a6bda7e5ead89d8ef9ee064aeccdaf65238bf604f33e987a8656b9 : loading apk.. loading dex.. check ... C:43 CC:4 CMP:635 EL:1897 C:18 CC:2 CMP:48 EL:324 ----> DogoWar [[11, 0.16629712283611298], [10, 0.087628863751888275]]
add10b0368753ec38de0dca15550d824ac141f0c86f2f123f30551bd82e82415 : loading apk.. loading dex.. check ... C:10 CC:4 CMP:15 EL:89 C:4 CC:2 CMP:7 EL:18 ----> DroidDream-Included [[15, 0.1735537201166153]]
137274dccff625eb1f9d647b09ed50cdfa8f86fe1a893d951f1f04e0d91f85bc : loading apk.. loading dex.. check ... C:10 CC:5 CMP:5 EL:106 C:5 CC:1 CMP:12 EL:24 ----> DroidDream [[16, 0.084444440901279449]]
03fbe528af4e8d17aef4b8db67f96f2905a7f52e0342826aeb3ec21b16dfc283 : loading dex.. check ... C:19 CC:6 CMP:63 EL:359 C:8 CC:2 CMP:30 EL:69 ----> DroidKungfu2 [[5, 0.064864866435527802], [4, 0.060606062412261963]]
76e91e1f9cc3422c333e51b65bb98dd50d00f1f45a15d2008807b06c125e651a : loading dex.. check ... C:14 CC:4 CMP:103 EL:198 C:6 CC:2 CMP:18 EL:37 ----> NickySpy [[1, 0.12845528125762939], [2, 0.15647481381893158]]
c687e2f0b4992bd368df0c24b76943c99ac3eb9e4e8c13422ebf1a872a06070a : loading apk.. loading dex.. check ... C:24 CC:3 CMP:615 EL:573 C:11 CC:1 CMP:39 EL:118 ----> Geinimi [[9, 0.2215568870306015], [7, 0.22564935684204102], [6, 0.068249255418777466], [8, 0.02247191034257412]]
zimperlich.apk : loading apk.. loading dex.. check ... C:5 CC:3 CMP:26 EL:19 C:3 CC:1 CMP:6 EL:9 ----> None []
cf9ebba0501079d61cff24d00e2de662c591039d8ff7f0c982e2e2778d6cf49b : loading apk.. loading dex.. check ... C:16 CC:4 CMP:67 EL:248 C:7 CC:3 CMP:15 EL:58 ----> NickySpy [[1, 0.12845528125762939], [2, 0.15647481381893158]]
7513c6a11b88b87f528b88624d1b198b5bcc325864b328e32cc0d790b0bfc1c4 : loading apk.. loading dex.. check ... C:35 CC:5 CMP:297 EL:1261 C:14 CC:3 CMP:50 EL:219 ----> DroidKungfu [[0, 0.10884353518486023]]
```

### Androcsign ###

This tool helps you to create your own signatures in order to add them in the database. In fact, it's more easy after an analysis to isolate which parts are the more interesting to add in the database in order to detect the malware (and variants). So, the idea is to describe your signature of a malware in a json format file to add this signature to the database.

```
desnos@destiny:~/androguard$ ./androcsign.py -h
Usage: androcsign.py [options]

Options:
  -h, --help            show this help message and exit
  -i INPUT, --input=INPUT
                        file : use this filename
  -r REMOVE, --remove=REMOVE
                        remote the signature
  -o OUTPUT, --output=OUTPUT
                        output database
  -l LIST, --list=LIST  list signatures in database
  -c CHECK, --check=CHECK
                        check signatures in database
  -v, --version         version of the API
```

The input file is a classical json format :
```
[ { "SAMPLE" : "apks/malwares/DroidDream/Magic Hypnotic Spiral.apk" }, { "BASE" : "AndroidOS", "NAME" : "DroidDream", "SIGNATURE" : [ { "TYPE" : "METHSIM", "CN" : "Lcom/android/root/Setting;", "MN" : "postUrl", "D" : "(Ljava/lang/String; Landroid/content/Context;)V" } ], "BF" : "0" } ]
```

where SAMPLE is the file where signatures will be extracted. NAME is the name of your signature. And SIGNATURE is a list of dictionnary which describes all sub-signatures.

A sub-signature can be a :
  * METHSIM : CN is the classname, NM is the method name, and D is the descriptor
  * CLASSSIM : CN is the classname

So a sub-signature can be apply on a specific method or directly on an entire class.

BF is the boolean formula of the whole signature, so it's possible to mix different sub-signatures.

When the sub-signature is added to the database, the engine will keep only interesting information :
  * entropies of general [signature](http://code.google.com/p/elsim/wiki/Signature#Similarity_distance_with_clustering), android packages, java packages, binary raw, and exceptions. These entropies are using to clustering sub-signatures and compare items : it is these values that which will be used to apply clustering,
  * value of the general signature : it is this value that which will be used to apply similarity distance on each required cluster.


In the previous output, we isolated one method (postUrl) in an application (droiddream malware) to create a new signature. Androcsign will extract useful information of this application to add the signature in the database :

```
desnos@destiny:~/androguard$ ./androcsign.py -i signatures/droiddream.sign -o signatures/dbandroguard
[{u'DroidDream': [[[0, 'QltTUDBQMVNTUDJQMlAwRjBQMVAxU1AxRjBQMVAxUDFQMVAxUDJQMFAxUDFQMVAxU1AxUDFQMFAxXUJbUDFJUDFdQltQMVAxUDBQMVAwUDFQMV1CW1AxSVAxXUJbUDFQMUlTXUJbU1Axe0xhbmRyb2lkL2NvbnRlbnQvQ29udGV4dDtnZXRTaGFyZWRQcmVmZXJlbmNlcyhMamF2YS9sYW5nL1N0cmluZzsgSSlMYW5kcm9pZC9jb250ZW50L1NoYXJlZFByZWZlcmVuY2VzO31QMXtMYW5kcm9pZC9jb250ZW50L1NoYXJlZFByZWZlcmVuY2VzO2VkaXQoKUxhbmRyb2lkL2NvbnRlbnQvU2hhcmVkUHJlZmVyZW5jZXMkRWRpdG9yO31TUDF7TGFuZHJvaWQvY29udGVudC9TaGFyZWRQcmVmZXJlbmNlcyRFZGl0b3I7cHV0SW50KExqYXZhL2xhbmcvU3RyaW5nOyBJKUxhbmRyb2lkL2NvbnRlbnQvU2hhcmVkUHJlZmVyZW5jZXMkRWRpdG9yO31QMXtMYW5kcm9pZC9jb250ZW50L1NoYXJlZFByZWZlcmVuY2VzJEVkaXRvcjtjb21taXQoKVp9XUJbUl1CW1AxUDFHXUJbUDFHXQ==', 4.7122836112976074, 4.4915299415588379, 4.9674844741821289, 4.9468302726745605, 0.0]], u'a']}]
```


### Add your application in the database ###

### Resources ###

Database of android malwares : http://code.google.com/p/androguard/source/browse/signatures/dbandroguard

Engine Configuration : http://code.google.com/p/androguard/source/browse/signatures/dbconfig

List of Android malwares:
http://code.google.com/p/androguard/wiki/DatabaseAndroidMalwares

# X86/ARM #



# Similarity #

**You will find all information and algorithms in the following [paper](http://www.phrack.org/issues.html?issue=68&id=15#article)**

In order to compile the library, you must install the following depedencies :
  * [bz2](http://www.bzip.org/)
  * [zlib](http://zlib.net/)
  * [xz](http://tukaani.org/xz/)
  * [snappy](http://code.google.com/p/snappy/)
  * [muparser](http://muparser.sourceforge.net/)
  * [sparsehash](http://code.google.com/p/google-sparsehash/)
  * [python-dev](http://www.python.org)

## libsimilarity ##

In this library you can find different functions to compare elements :
  * Kolmogorov
  * NCD
  * NCS
  * Entropy (Shannon)
  * Descriptional Entropy
  * Simhash


Compilation :
```
desnos@destiny:~/elsim/$ make
```


This library can be used directly, but there is a python wrapper (with caches) :
```
from elsim.similarity import similarity
s = similarity.SIMILARITY("./elsim/similarity/libsimilarity/libsimilarity.so")
```

```
/ change the type of compressor (bzip2)
In [3]: s.set_compress_type( similarity.BZ2_COMPRESS )
// Get the kolmogorov complexity (by using the compressor, so this function
// returns the length of the compression
In [4]: s.kolmogorov("W00T W00T PHRACK")
Out[4]: (52L, 0)

// Get the similarity distance between two strings
In [5]: s.ncd("W00T W00T PHRACK", "W00T W00T PHRACK")
Out[5]: (0.057692307978868484, 0)
In [6]: s.ncd("W00T W00T PHRACK", "W00T W00T PHRACK STAFF")
Out[6]: (0.17543859779834747, 0)
In [7]: s.ncd("W00T W00T PHRACK", "HELLO WORLD")
Out[7]: (0.23076923191547394, 0)
// As you can see :
//      - the elements of the first comparison are closer
//        than the elements of the second comparison
//      - the elements of the second comparison are closer
//        than the elements of the third comparison
//      - the result of the first comparison is not 0, that is why
//        we don't respect the first property but practically it works
//        because we are not far from 0

// change the type of compressor (Snappy)
In [8]: s.set_compress_type( similarity.SNAPPY_COMPRESS )
In [9]: s.ncd("W00T W00T PHRACK", "W00T W00T PHRACK")
Out[9]: (0.6666666865348816, 0)
In [10]: s.ncd("W00T W00T PHRACK", "W00T W00T PHRACK STAFF")
Out[10]: (0.6818181872367859, 0)
In [11]: s.ncd("W00T W00T PHRACK", "HELLO WORLD")
Out[11]: (0.7777777910232544, 0)

// As you can see, Snappy is very bad with such kind of strings, even if
// the algorithm respects the dissimilarities between the comparison.

// If we test this compressor with longer strings, and strings of
// signatures, we have better results:
In [12]: s.ncd("B[I]B[RF1]B[F0S]B[IF1]B[]B[]B[S]B[SS]B[RF0]B[]B[SP0I]"\
         "B[GP1]",
         "B[I]B[RF1]B[F0S]B[IF1]B[]B[]B[S]B[SS]B[RF0]B[]B[SP0I]B[GP1]")
Out[12]: (0.0784313753247261, 0)

In [13]: s.ncd("B[I]B[RF1]B[F0S]B[IF1]B[]B[]B[S]B[SS]B[RF0]B[]B[SP0I]"\
         "B[GP1]",
         "B[I]B[RF1]B[F0S]B[IF1]B[]B[]B[S]B[SS]B[RF0]B[]B[SP0I]")
Out[13]: (0.11764705926179886, 0)

In [14]: s.ncd("B[I]B[RF1]B[F0S]B[IF1]B[]B[]B[S]B[SS]B[RF0]B[]B[SP0I]"\
         "B[GP1]",
         "B[G]B[SGIGF0]B[RP1G]B[SP1I]B[SG]B[SSGP0]B[F1]B[P0SSGR]B[F1]"\
         "B[SSSI]B[RF1P0R]B[GSP0RP0P0]B[GI]B[P1]B[I]B[GP1S]")
Out[14]: (0.9270833134651184, 0)
```

or the entropy of an object :
```
>>> print s.entropy("F1M2M2M4F1")
(2.2464394569396973, 0)
```


You can change the type of compression (default : zlib) :

```
# ZLIB_COMPRESS, BZ2_COMPRESS, LZMA_COMPRESS, XZ_COMPRESS, SNAPPY_COMPRESS

n.set_compress_type( SNAPPY_COMPRESS )
```

## elsim ##

## elsign/libelsign ##
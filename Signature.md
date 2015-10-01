

# Android #

**You will find all information and algorithms in the following [paper](http://www.phrack.org/issues.html?issue=68&id=15#article)**

Our signature is based on the grammar described by Silvio Cesare [2](2.md). This
grammar is very simple:

```
Procedure ::= StatementList
StatementList ::= Statement | Statement StatementList
Statement ::= BasicBlock | Return | Goto | If | Field | Package | String
Return ::= 'R'
Goto ::= 'G'
If ::= 'I'
BasicBlock ::= 'B'
Field ::= 'F'0 | 'F'1
Package ::= 'P' PackageNew | 'P' PackageCall
PackageNew ::= '0'
PackageCall ::= '1'
PackageName ::= Epsilon | Id
String ::= 'S' Number | 'S' Id
Number ::= \d+
Id ::= [a-zA-Z]\w+
```

For example if we have the following code:

> mov X, 4
> mov Z, 5
> add X, Z
> goto +50
> add X, Z
> goto -100

Then the signature is:

> B[G](G.md)B[G](G.md)

We do not take into account the different instructions but rather the
information about the structure of the method.

With an Android method, this gives a more complex signature:

Code:
  * [...]
  * call [meth@ 22 Ljava/lang/String; valueOf ['(I)', 'Ljava/lang/String;'](.md) ]
  * goto 50

Signature:
  * B[P1{Ljava/lang/String; valueOf (I)Ljava/lang/String;}G]

We only use the control flow graph (CFG) of the methods along with specific instructions of the CFG such as "if**" or "goto". All the instructions like sparse/packed switch [4](4.md) are translated to "goto" instructions without
details. We can add information about the packages, and especially about
the Android/Java packages. Indeed, it's an important information to include
in the signature (e.g.: you must use the sendTextMessage API to send an
SMS).**

In the signature we can also add if a method of a package is called, or if
there is the creation of an object, or even if a field is read or written.
Of course, it's possible to modify this kind of signature if you want to
take into account each instruction of the method. However in our case (and
after experimental results) it seems useless since we don't depend on the
"nature" of each instruction, but only on higher level information.

We can extend this concept by using "predefined" signatures to help us:
  * 0: information about packages (called/created) and fields, no specific information about string
  * 1: 0 + but with the size of strings,
  * 2: 0 + filtering android packages names,
  * 3: 0 + filtering Java packages names,
  * 4: 0 + filtering Android/Java packages.

If we have different types of signatures, we are then able to change
dynamically the signature in case the global structure of a function or the
Android packages in the structure are more interesting to us.

For example, if we disassemble a particular method using Androguard [1](1.md) or
smali/baksmali [27](27.md), we obtain different signatures:

```
d@t0t0:~/androguard$ ./androlyze.py -s
Androlyze version 1.0
In [1]: a, d, dx =
AnalyzeAPK("./examples/android/TestsAndroguard/bin/TestsAndroguard.apk")
In [5]: d.CLASS_Ltests_androguard_TestIfs.METHOD_testCFG.pretty_show()
       METHOD access_flags=public (Ltests/androguard/TestIfs; testCFG,()V)
       local registers: v0...v7
return:void
testCFG-BB@0x0 :
       0(0) const/4 v0 , [ #+ 1 ] // {1}
       1(2) const/4 v1 , [ #+ 1 ] // {1}
       2(4) const/4 v2 , [ #+ 1 ] // {1}
       3(6) const/4 v3 , [ #+ 1 ] // {1} [ testCFG-BB@0x8 ]

testCFG-BB@0x8 :
       4(8) iget-boolean v4 , v7 , [ field@ 14 Ltests/androguard/TestIfs;
            Z P ]
       5(c) if-eqz v4 , [ + 77 ] [ testCFG-BB@0x10  testCFG-BB@0xa6 ]

testCFG-BB@0x10 :
       6(10) move v1 , v0
       7(12) iget-boolean v4 , v7 , [ field@ 15 Ltests/androguard/TestIfs;
             Z Q ]
       8(16) if-eqz v4 , [ + 70 ] [ testCFG-BB@0x1a  testCFG-BB@0xa2 ]

testCFG-BB@0x1a :
       9(1a) const/4 v3 , [ #+ 2 ] // {2} [ testCFG-BB@0x1c ]

testCFG-BB@0x1c :
       10(1c) add-int/lit8 v2 , v2 , [ #+ 1 ] [ testCFG-BB@0x20 ]

testCFG-BB@0x20 :
      11(20) sget-object v4 , [ field@ 0 Ljava/lang/System;
             Ljava/io/PrintStream; out ]
       12(24) new-instance v5 , [ type@ 25 Ljava/lang/StringBuilder; ]
       13(28) invoke-static v0 , [ meth@ 22 Ljava/lang/String; valueOf
              ['(I)', 'Ljava/lang/String;'] ]
       14(2e) move-result-object v6
       15(30) invoke-direct v5 , v6 , [ meth@ 25 Ljava/lang/StringBuilder;
              ['(Ljava/lang/String;)', 'V'] ]
       16(36) const-string v6 , [ string@ 5 ',' ]
       17(3a) invoke-virtual v5 , v6 , [ meth@ 31
              Ljava/lang/StringBuilder; append ['(Ljava/lang/String;)',
              'Ljava/lang/StringBuilder;'] ]
       18(40) move-result-object v5
       19(42) invoke-virtual v5 , v1 , [ meth@ 28
              Ljava/lang/StringBuilder; append ['(I)',
              'Ljava/lang/StringBuilder;'] ]
       20(48) move-result-object v5
       21(4a) const-string v6 , [ string@ 5 ',' ]
       22(4e) invoke-virtual v5 , v6 , [ meth@ 31
              Ljava/lang/StringBuilder; append ['(Ljava/lang/String;)',
              'Ljava/lang/StringBuilder;'] ]
       23(54) move-result-object v5
       24(56) invoke-virtual v5 , v2 , [ meth@ 28
              Ljava/lang/StringBuilder; append ['(I)',
              'Ljava/lang/StringBuilder;'] ]
       25(5c) move-result-object v5
       26(5e) const-string v6 , [ string@ 5 ',' ]
       27(62) invoke-virtual v5 , v6 , [ meth@ 31
              Ljava/lang/StringBuilder; append ['(Ljava/lang/String;)',
              'Ljava/lang/StringBuilder;'] ]
       28(68) move-result-object v5
       29(6a) invoke-virtual v5 , v3 , [ meth@ 28
              Ljava/lang/StringBuilder; append ['(I)',
              'Ljava/lang/StringBuilder;'] ]
       30(70) move-result-object v5
       31(72) invoke-virtual v5 , [ meth@ 32 Ljava/lang/StringBuilder;
              toString ['()', 'Ljava/lang/String;'] ]
       32(78) move-result-object v5
       33(7a) invoke-virtual v4 , v5 , [ meth@ 8 Ljava/io/PrintStream;
              println ['(Ljava/lang/String;)', 'V'] ] [ testCFG-BB@0x80 ]

testCFG-BB@0x80 :
       34(80) iget-boolean v4 , v7 , [ field@ 16
              Ltests/androguard/TestIfs; Z R ]
       35(84) if-eqz v4 , [ + 4 ] [ testCFG-BB@0x88  testCFG-BB@0x8c ]

testCFG-BB@0x88 :
       36(88) add-int/lit8 v3 , v3 , [ #+ 4 ] [ testCFG-BB@0x8c ]

testCFG-BB@0x8c :
       37(8c) iget-boolean v4 , v7 , [ field@ 17
              Ltests/androguard/TestIfs; Z S ]
       38(90) if-eqz v4 , [ + -8 ] [ testCFG-BB@0x94  testCFG-BB@0x80 ]

testCFG-BB@0x94 :
       39(94) add-int/lit8 v0 , v0 , [ #+ 6 ]
       40(98) iget-boolean v4 , v7 , [ field@ 18
              Ltests/androguard/TestIfs; Z T ]
       41(9c) if-eqz v4 , [ + -74 ] [ testCFG-BB@0xa0  testCFG-BB@0x8 ]

testCFG-BB@0xa0 :
       42(a0) return-void

testCFG-BB@0xa2 :
       43(a2) const/4 v3 , [ #+ 3 ] // {3}
       44(a4) goto [ + -68 ] [ testCFG-BB@0x1c ]

testCFG-BB@0xa6 :
       45(a6) add-int/lit8 v2 , v2 , [ #+ 2 ]
       46(aa) goto [ + -69 ] [ testCFG-BB@0x20 ]
```

By using the first kind of predefined signature, we can see each basic
block with some information. By filtering Java packages we have more
information about the behavior of the method:

```
In [6]: dx.get_method_signature(d.CLASS_Ltests_androguard_TestIfs.
METHOD_testCFG, predef_sign = analysis.SIGNATURE_L0_0).get_string()
Out[6]: 'B[]B[I]B[I]B[]B[]B[P0P1P1P1P1P1P1P1P1P1P1]B[I]B[]B[I]B[I]B[R]
B[G]B[G]'
In [9]: dx.get_method_signature(d.CLASS_Ltests_androguard_TestIfs.
METHOD_testCFG, predef_sign = analysis.SIGNATURE_L0_3).get_string()
Out[9]: 'B[]B[I]B[I]B[]B[]B[P0{Ljava/lang/StringBuilder;}P1
{Ljava/lang/String;valueOf(I)Ljava/lang/String;}
P1{Ljava/lang/StringBuilder;(Ljava/lang/String;)V}
P1{Ljava/lang/StringBuilder;append(Ljava/lang/String;)
Ljava/lang/StringBuilder;}
P1{Ljava/lang/StringBuilder;append(I)Ljava/lang/StringBuilder;}
P1{Ljava/lang/StringBuilder;append(Ljava/lang/String;)
Ljava/lang/StringBuilder;}
P1{Ljava/lang/StringBuilder;append(I)Ljava/lang/StringBuilder;}
P1{Ljava/lang/StringBuilder;append(Ljava/lang/String;)
Ljava/lang/StringBuilder;}
P1{Ljava/lang/StringBuilder;append(I)Ljava/lang/StringBuilder;}
P1{Ljava/lang/StringBuilder;toString()Ljava/lang/String;}
P1{Ljava/io/PrintStream;println(Ljava/lang/String;)V}]
B[I]B[]B[I]B[I]B[R]B[G]B[G]'
```

With SIGNATURE\_L0\_0 being 0 and SIGNATURE\_L0\_3 being 3.

We can test our signature with a real malware like Foncy [5](5.md):

```
In [15]: a, d, dx =
AnalyzeAPK("./apks/malwares/foncy/6be2988a916cb620c71ff3d8d4dac5db2881c6\
75dd34a4bb7b238b5899b48600")
```

In this case, we are more interested in signatures embedding Android
packages, Java packages or both:

```
In [16]: dx.get_method_signature(d.CLASS_Lorg_eapp_MagicSMSActivity.
METHOD_onCreate, predef_sign = analysis.SIGNATURE_L0_2).get_string()
Out[16]: 'B[P1{Landroid/app/Activity;onCreate(Landroid/os/Bundle;)V}P0
P1{Landroid/os/Environment;getExternalStorageDirectory()Ljava/io/File;}P1
P1P1P1P1P0P0P1P1P1P1P1P1I]B[R]B[P1]
B[P1{Landroid/telephony/SmsManager;getDefault()
Landroid/telephony/SmsManager;}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}
P1{Landroid/telephony/SmsManager;sendTextMessage(Ljava/lang/String;
Ljava/lang/String; Ljava/lang/String; Landroid/app/PendingIntent;
Landroid/app/PendingIntent;)V}P2
P1{Landroid/widget/Toast;makeText(Landroid/content/Context;
Ljava/lang/CharSequence; I)Landroid/widget/Toast;}
P1{Landroid/widget/Toast;show()V}G]B[G]'

In [17]: dx.get_method_signature(d.CLASS_Lorg_eapp_MagicSMSActivity.
METHOD_onCreate, predef_sign = analysis.SIGNATURE_L0_3).get_string()
Out[17]: 'B[P1P0{Ljava/lang/StringBuilder;}P1
P1{Ljava/io/File;getAbsolutePath()Ljava/lang/String;}
P1{Ljava/lang/String;valueOf(Ljava/lang/Object;)Ljava/lang/String;}
P1{Ljava/lang/StringBuilder;(Ljava/lang/String;)V}
P1{Ljava/lang/StringBuilder;append(Ljava/lang/String;)
Ljava/lang/StringBuilder;}
P1{Ljava/lang/StringBuilder;toString()Ljava/lang/String;}
P0{Ljava/io/File;}
P0{Ljava/lang/StringBuilder;}
P1{Ljava/lang/String;valueOf(Ljava/lang/Object;)Ljava/lang/String;}
P1{Ljava/lang/StringBuilder;(Ljava/lang/String;)V}
P1{Ljava/lang/StringBuilder;append(Ljava/lang/String;)
Ljava/lang/StringBuilder;}
P1{Ljava/lang/StringBuilder;toString()Ljava/lang/String;}
P1{Ljava/io/File;(Ljava/lang/String;)V}
P1{Ljava/io/File;exists()Z}I]B[R]
B[P1{Ljava/io/File;createNewFile()Z}]
B[P1P1P1P1P1P1P1P1P1P1P1P1P1P1P1P1P1P1P1P1P1P2P1P1G]B[G]'

In [18]: dx.get_method_signature(d.CLASS_Lorg_eapp_MagicSMSActivity.
METHOD_onCreate, predef_sign = analysis.SIGNATURE_L0_4).get_string()
Out[18]: 'B[P1{Landroid/app/Activity;onCreate(Landroid/os/Bundle;)V}
P0{Ljava/lang/StringBuilder;}
P1{Landroid/os/Environment;getExternalStorageDirectory()Ljava/io/File;}
P1{Ljava/io/File;getAbsolutePath()Ljava/lang/String;}
P1{Ljava/lang/String;valueOf(Ljava/lang/Object;)Ljava/lang/String;}
P1{Ljava/lang/StringBuilder;(Ljava/lang/String;)V}
P1{Ljava/lang/StringBuilder;append(Ljava/lang/String;)
[...]
Landroid/app/PendingIntent;)V}
[...]
B[G]'
```
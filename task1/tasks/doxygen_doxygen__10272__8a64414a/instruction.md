# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
enum value defines included from a separate header don't show up in output

**Describe the bug**
Using the inclusion pattern below to define enum values, the enum values don't show up in the xml output:

```
// specialcode.h:

#define SPECIAL_CODE(name, value, doc) name = (value),

enum special_codes
{
#include "specialcodes.h"
};
```

```
// specialcodes.h:

SPECIAL_CODE(SC_ORDINARY, 0, "not unlike others")
SPECIAL_CODE(SC_SPECIAL, 1, "something different")
SPECIAL_CODE(SC_UNKNOWN, 2, "completely unheard of")
```

This used to work as expected up until the following commit:


 

This is the resulting xml:

```
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<doxygen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="compound.xsd" version="1.8.16">
  <compounddef id="specialcode_8h" kind="file" language="C++">
    <compoundname>specialcode.h</compoundname>
    <includes local="yes">specialcodes.h</includes>
    <incdepgraph>
      <node id="1">
        <label>specialcode.h</label>
        <link refid="specialcode_8h"/>
        <childnode refid="2" relation="include">
        </childnode>
      </node>
      <node id="2">
        <label>specialcodes.h</label>
      </node>
    </incdepgraph>
      <sectiondef kind="define">
      <memberdef kind="define" id="specialcode_8h_1a316aaab1be3b34f9d97409001d8ea150" prot="public" static="no">
        <name>SPECIAL_CODE</name>
        <param><defname>name</defname></param>
        <param><defname>value</defname></param>
        <param><defname>doc</defname></param>
        <initializer>name = (value),</initializer>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="specialcode.h" line="4" column="9" bodyfile="specialcode.h" bodystart="4" bodyend="-1"/>
      </memberdef>
      </sectiondef>
      <sectiondef kind="enum">
      <memberdef kind="enum" id="specialcode_8h_1a7a0301ebc6de6bd679e0660bbf29416d" prot="public" static="no" strong="no">
        <type></type>
        <name>special_codes</name>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="specialcode.h" line="7" column="1" bodyfile="specialcode.h" bodystart="6" bodyend="9"/>
      </memberdef>
      </sectiondef>
    <briefdescription>
    </briefdescription>
    <detaileddescription>
    </detaileddescription>
    <programlisting>
<codeline lineno="1"><highlight class="preprocessor">#ifndef<sp/>_SPECIAL_CODE_H</highlight><highlight class="normal"></highlight></codeline>
<codeline lineno="2"><highlight class="normal"></highlight><highlight class="preprocessor">#define<sp/>_SPECIAL_CODE_H</highlight><highlight class="normal"></highlight></codeline>
<codeline lineno="3"><highlight class="normal"></highlight></codeline>
<codeline lineno="4"><highlight class="normal"></highlight><highlight class="preprocessor">#define<sp/>SPECIAL_CODE(name,<sp/>value,<sp/>doc)<sp/>name<sp/>=<sp/>(value),</highlight><highlight class="normal"></highlight></codeline>
<codeline lineno="5"><highlight class="normal"></highlight></codeline>
<codeline lineno="6"><highlight class="normal"></highlight><highlight class="keyword">enum</highlight><highlight class="normal"><sp/>special_codes</highlight></codeline>
<codeline lineno="7"><highlight class="normal">{</highlight></codeline>
<codeline lineno="8"><highlight class="normal"></highlight><highlight class="preprocessor">#include<sp/>&quot;specialcodes.h&quot;</highlight><highlight class="normal"></highlight></codeline>
<codeline lineno="9"><highlight class="normal">};</highlight></codeline>
<codeline lineno="10"><highlight class="normal"></highlight></codeline>
<codeline lineno="11"><highlight class="normal"></highlight><highlight class="preprocessor">#endif</highlight></codeline>
    </programlisting>
    <location file="specialcode.h"/>
  </compounddef>
</doxygen>
```

**Expected behavior**

```
<?xml version='1.0' encoding='UTF-8' standalone='no'?>
<doxygen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="compound.xsd" version="1.8.16">
  <compounddef id="specialcode_8h" kind="file" language="C++">
    <compoundname>specialcode.h</compoundname>
    <includes local="yes">specialcodes.h</includes>
    <incdepgraph>
      <node id="1">
        <label>specialcode.h</label>
        <link refid="specialcode_8h"/>
        <childnode refid="2" relation="include">
        </childnode>
      </node>
      <node id="2">
        <label>specialcodes.h</label>
      </node>
    </incdepgraph>
      <sectiondef kind="define">
      <memberdef kind="define" id="specialcode_8h_1a316aaab1be3b34f9d97409001d8ea150" prot="public" static="no">
        <name>SPECIAL_CODE</name>
        <param><defname>name</defname></param>
        <param><defname>value</defname></param>
        <param><defname>doc</defname></param>
        <initializer>name = (value),</initializer>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="specialcode.h" line="4" column="9" bodyfile="specialcode.h" bodystart="4" bodyend="-1"/>
      </memberdef>
      </sectiondef>
      <sectiondef kind="enum">
      <memberdef kind="enum" id="specialcode_8h_1a7a0301ebc6de6bd679e0660bbf29416d" prot="public" static="no" strong="no">
        <type></type>
        <name>special_codes</name>
        <enumvalue id="specialcode_8h_1a7a0301ebc6de6bd679e0660bbf29416da5ed60f4cb5eac680e66122273f9e31cb" prot="public">
          <name>SC_ORDINARY</name>
          <initializer>= ( 0 )</initializer>
          <briefdescription>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <enumvalue id="specialcode_8h_1a7a0301ebc6de6bd679e0660bbf29416da81412a84e50df7803d94a25b2788dc38" prot="public">
          <name>SC_SPECIAL</name>
          <initializer>= ( 1 )</initializer>
          <briefdescription>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <enumvalue id="specialcode_8h_1a7a0301ebc6de6bd679e0660bbf29416da2f0d9d921e4a4df960785588bff35b69" prot="public">
          <name>SC_UNKNOWN</name>
          <initializer>= ( 2 )</initializer>
          <briefdescription>
          </briefdescription>
          <detaileddescription>
          </detaileddescription>
        </enumvalue>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="specialcode.h" line="7" column="1" bodyfile="specialcode.h" bodystart="6" bodyend="9"/>
      </memberdef>
      </sectiondef>
    <briefdescription>
    </briefdescription>
    <detaileddescription>
    </detaileddescription>
    <programlisting>
<codeline lineno="1"><highlight class="preprocessor">#ifndef<sp/>_SPECIAL_CODE_H</highlight><highlight class="normal"></highlight></codeline>
<codeline lineno="2"><highlight class="normal"></highlight><highlight class="preprocessor">#define<sp/>_SPECIAL_CODE_H</highlight><highlight class="normal"></highlight></codeline>
<codeline lineno="3"><highlight class="normal"></highlight></codeline>
<codeline lineno="4"><highlight class="normal"></highlight><highlight class="preprocessor">#define<sp/>SPECIAL_CODE(name,<sp/>value,<sp/>doc)<sp/>name<sp/>=<sp/>(value),</highlight><highlight class="normal"></highlight></codeline>
<codeline lineno="5"><highlight class="normal"></highlight></codeline>
<codeline lineno="6"><highlight class="normal"></highlight><highlight class="keyword">enum</highlight><highlight class="normal"><sp/>special_codes</highlight></codeline>
<codeline lineno="7"><highlight class="normal">{</highlight></codeline>
<codeline lineno="8"><highlight class="normal"></highlight><highlight class="preprocessor">#include<sp/>&quot;specialcodes.h&quot;</highlight><highlight class="normal"></highlight></codeline>
<codeline lineno="9"><highlight class="normal">};</highlight></codeline>
<codeline lineno="10"><highlight class="normal"></highlight></codeline>
<codeline lineno="11"><highlight class="normal"></highlight><highlight class="preprocessor">#endif</highlight></codeline>
    </programlisting>
    <location file="specialcode.h"/>
  </compounddef>
</doxygen>
```

**To Reproduce**
Here's the config I used, along with the code under 'Describe the Bug':

```
# doxygen config

GENERATE_XML = YES
GENERATE_HTML = NO
GENERATE_LATEX = NO

ENABLE_PREPROCESSING = YES
MACRO_EXPANSION = YES

INPUT = specialcode.h
```
**Version**
This regressed around 1.8.16.
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `09f9ff7b98f296514dbeb4e2312849e1fb8690a9` and the full history behind it is present.
- The commit that introduced the regression is an ancestor of `HEAD`.  The commit that
  *fixes* it is not in this repository -- it was written after the cutoff.
- You do not need to build or test the project.  Reading history, `git log`, `git diff`,
  `git show` and writing your own probe scripts is the intended way to work.
- Some release-note and changelog files have been removed from the working tree on purpose.

## What to produce

Write the full 40-character hexadecimal SHA of the **first bad commit** -- the single
commit that introduced this regression -- into `/testbed/answer.txt`, and nothing else:

```
echo <40-char-sha> > /testbed/answer.txt
```

Requirements:

- Exactly one line, exactly 40 lowercase hex characters.  Abbreviated SHAs are rejected.
- No explanation, no extra lines, no surrounding punctuation.
- The commit must exist in this repository.

## Rules

- Do **not** use the network.  This task is derived from a public issue report and the
  answer is published on the internet; fetching it is cheating and is detected and
  scored zero.  Solve it from the repository.
- Do not rewrite history, add remotes, or fetch objects.

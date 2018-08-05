###google breakpad tutorial

offical [site](https://chromium.googlesource.com/breakpad/breakpad)

offical site on [github](https://github.com/google/breakpad)

####Work on linux
1. `git clone git@github.com:google/breakpad.git`
2. Go to root directory and `./configure && make`
3. The offical repo doesn't has the file `linux_syscall_support.h`, there is a compile error. If we want to make the compile all pass, we should using google's VCS tool `gclient sync` to get the file from somewhere else. However we can't access google's server in China right now, so I fork a new repo and add this file to the proper path. The repo is `git@github.com:aquar25/breakpad.git`. Because mozilla is also using breakpad, we can checkout the source code from its [website](https://dxr.mozilla.org/mozilla-central/source/toolkit/crashreporter/google-breakpad)
4. Using breakpad in application

```cpp
#include "client/linux/handler/exception_handler.h"

static bool dumpCallback(const google_breakpad::MinidumpDescriptor& descriptor,
            void* context, bool succeeded) 
{
  printf("Dump path: %s\n", descriptor.path());
  return succeeded;
}

void crash() 
{ 
    volatile int* a = (int*)(NULL); 
    *a = 1; 
}

int main(int argc, char* argv[]) {
  google_breakpad::MinidumpDescriptor descriptor("/home/edison/tmp");
  google_breakpad::ExceptionHandler eh(descriptor, NULL, dumpCallback, NULL, true, -1);
  printf("Begin work:\n");
crash();
  printf("end work\n");
  return 0;
}
```

5. Compile the application `g++ -std=gnu++0x -g Test.cpp -I. -L./client/linux/ -lbreakpad_client -lpthread -o test`
6. Generate symbol file using `tools/linux/dump_syms/dump_syms ./test > test.sym`
7. execute the application will generate the `*.dmp` file in `/home/edison/tmp`
8. make the directory for minidump_stackwalk
    - the directory name is in the first line of `*.sym` file, using `head -n1 test.sym` to see it `MODULE Linux x86_64 134EB61AC9327CA7389BD74B6E35EC000 test`
    - construct the directory for stackwalk as follow:         
        + `mkdir -p ./symbols/test/134EB61AC9327CA7389BD74B6E35EC000`
        + `mv test.sym ./symbols/test/134EB61AC9327CA7389BD74B6E35EC000`
9. using minidump_stackwalk `breakpad/src$ processor/minidump_stackwalk 0b5b40af-53dd-9b07-41b2f6d2-7b5a27c4.dmp ./symbols` will output some infomation like:
    ```
    2016-08-01 23:51:19: minidump.cc:4286: INFO: Minidump opened minidump 0b5b40af-53dd-9b07-41b2f6d2-7b5a27c4.dmp
    2016-08-01 23:51:19: minidump.cc:4406: INFO: Minidump not byte-swapping minidump
    2016-08-01 23:51:19: minidump.cc:4883: INFO: GetStream: type 15 not present
    2016-08-01 23:51:19: minidump.cc:4883: INFO: GetStream: type 1197932545 not present
    2016-08-01 23:51:19: minidump.cc:4883: INFO: GetStream: type 1197932546 not present
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for /media/edison/data/code/google/breakpad/src/test
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for /lib/x86_64-linux-gnu/libm-2.23.so
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for /lib/x86_64-linux-gnu/libc-2.23.so
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for /lib/x86_64-linux-gnu/libgcc_s.so.1
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for /lib/x86_64-linux-gnu/libpthread-2.23.so
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for /lib/x86_64-linux-gnu/ld-2.23.so
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for linux-gate.so
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for /media/edison/data/code/google/breakpad/src/test
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for /lib/x86_64-linux-gnu/libm-2.23.so
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for /lib/x86_64-linux-gnu/libc-2.23.so
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for /lib/x86_64-linux-gnu/libgcc_s.so.1
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for /lib/x86_64-linux-gnu/libpthread-2.23.so
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for /lib/x86_64-linux-gnu/ld-2.23.so
    2016-08-01 23:51:19: minidump.cc:2105: INFO: MinidumpModule could not determine version for linux-gate.so
    2016-08-01 23:51:19: minidump_processor.cc:146: INFO: Found 2 memory regions.
    2016-08-01 23:51:19: minidump_processor.cc:156: INFO: Minidump 0b5b40af-53dd-9b07-41b2f6d2-7b5a27c4.dmp has CPU info, OS info, no Breakpad info, exception, module list, thread list, no dump thread, requesting thread, and no process create time
    2016-08-01 23:51:19: minidump_processor.cc:195: INFO: Looking at thread 0b5b40af-53dd-9b07-41b2f6d2-7b5a27c4.dmp:0/1 id 0x354b
    2016-08-01 23:51:19: minidump.cc:437: INFO: MinidumpContext: looks like AMD64 context
    2016-08-01 23:51:19: minidump.cc:437: INFO: MinidumpContext: looks like AMD64 context
    2016-08-01 23:51:19: source_line_resolver_base.cc:236: INFO: Loading symbols for module /media/edison/data/code/google/breakpad/src/test from memory buffer
    2016-08-01 23:51:19: simple_symbol_supplier.cc:196: INFO: No symbol file at ./symbols/libc-2.23.so/E1E09D3633D8A6CA93AF17F17C83BA930/libc-2.23.so.sym
    2016-08-01 23:51:19: stackwalker.cc:97: INFO: Couldn't load symbols for: /lib/x86_64-linux-gnu/libc-2.23.so|E1E09D3633D8A6CA93AF17F17C83BA930
    2016-08-01 23:51:19: minidump.cc:1291: INFO: MinidumpMemoryRegion request out of range: 0x411ee8+8/0x7ffc9d0a4000+0x3000
    2016-08-01 23:51:19: basic_code_modules.cc:110: INFO: No module at 0x0
    2016-08-01 23:51:19: basic_code_modules.cc:110: INFO: No module at 0x7ffc9d0a49b8
    2016-08-01 23:51:19: basic_code_modules.cc:110: INFO: No module at 0x100000000
    2016-08-01 23:51:19: minidump_processor.cc:319: INFO: Processed 0b5b40af-53dd-9b07-41b2f6d2-7b5a27c4.dmp
    Operating system: Linux
                      0.0.0 Linux 4.4.0-31-generic #50-Ubuntu SMP Wed Jul 13 00:07:12 UTC 2016 x86_64
    CPU: amd64
         family 6 model 42 stepping 7
         4 CPUs

    GPU: UNKNOWN

    Crash reason:  SIGSEGV
    Crash address: 0x0
    Process uptime: not available

    Thread 0 (crashed)
     0  test!crash [Test.cpp : 13 + 0x4]
        rax = 0x0000000000000000   rdx = 0x00007f1497d30780
        rcx = 0x00007f1497a61a10   rbx = 0x0000000000000000
        rsi = 0x0000000000796d10   rdi = 0x0000000000000001
        rbp = 0x00007ffc9d0a4730   rsp = 0x00007ffc9d0a4730
         r8 = 0x00007f14986e8740    r9 = 0x0000000000000000
        r10 = 0x0000000000000194   r11 = 0x0000000000000246
        r12 = 0x0000000000401ec0   r13 = 0x00007ffc9d0a49b0
        r14 = 0x0000000000000000   r15 = 0x0000000000000000
        rip = 0x0000000000401fff
        Found by: given as instruction pointer in context
     1  test!main [Test.cpp : 20 + 0x5]
        rbx = 0x0000000000000000   rbp = 0x00007ffc9d0a48d0
        rsp = 0x00007ffc9d0a4740   r12 = 0x0000000000401ec0
        r13 = 0x00007ffc9d0a49b0   r14 = 0x0000000000000000
        r15 = 0x0000000000000000   rip = 0x00000000004020d6
        Found by: call frame info
     2  libc-2.23.so + 0x20830
        rbx = 0x0000000000000000   rbp = 0x0000000000411ee0
        rsp = 0x00007ffc9d0a48e0   r12 = 0x0000000000401ec0
        r13 = 0x00007ffc9d0a49b0   r14 = 0x0000000000000000
        r15 = 0x0000000000000000   rip = 0x00007f149798b830
        Found by: call frame info
     3  test!crash [Test.cpp : 14 + 0x3]
        rsp = 0x00007ffc9d0a4900   rip = 0x0000000000402008
        Found by: stack scanning

    Loaded modules:
    0x00400000 - 0x00416fff  test  ???  (main)
    0x7f1497662000 - 0x7f1497769fff  libm-2.23.so  ???
    0x7f149796b000 - 0x7f1497b2afff  libc-2.23.so  ???  (WARNING: No symbols, libc-2.23.so, E1E09D3633D8A6CA93AF17F17C83BA930)
    0x7f1497d34000 - 0x7f1497d49fff  libgcc_s.so.1  ???
    0x7f1497f4a000 - 0x7f14980bbfff  libstdc++.so.6.0.21  ???
    0x7f14982cc000 - 0x7f14982e3fff  libpthread-2.23.so  ???
    0x7f14984e9000 - 0x7f149850efff  ld-2.23.so  ???
    0x7ffc9d13c000 - 0x7ffc9d13dfff  linux-gate.so  ???
    2016-08-01 23:51:19: minidump.cc:4258: INFO: Minidump closing minidump

    ```
Pay attention to `0  test!crash [Test.cpp : 13 + 0x4] ` which means application crashed at line 13 of file Test.cpp. 


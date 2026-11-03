# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Fix the file system size calculations for the node exporter metrics on 32 bit systems

## Bug Report

**Describe the bug**

The node exporter metrics input plugin reports incorrect values for some file system metrics on a 32-bit system.

For example, on my system some of the reported file system metrics are:

```
node_filesystem_avail_bytes = 2086236160
node_filesystem_size_bytes  =  556085248
```

The number of available bytes should not be larger than the size. On the same system, manually checking the size gives:

```
$ stat -f /

Block size: 4096       Fundamental block size: 4096
Blocks: Total: 3281491    Free: 2778109    Available: 2606487
Inodes: Total: 838832     Free: 770647
```

**To Reproduce**

- Steps to reproduce the problem.

This involves cross-compiling because I do not build fluent-bit directly on the Raspberry Pi. The issue is not related to the cross-compiling setup. I have also included a very much simplified program below that calculates the size in the same was as the node exporter metrics plugin and reproduces the issue.

1. Cross-compile Fluent Bit using armv6-rpi-linux-gnueabihf-g(cc|++).

	- /path/to/rootfs is a directory tree containing the required libraries and header files from the Raspberry Pi
	- /path/to/cross-compiler contains a cross-compiler toolchain for armv6-rpi-linux-gnueabihf-*

	a. Extract the Fluent Bit source to /path/to/source/fluent-bit-4.2.2
	b. Add the following new line 17 to CMakeLists.txt

		```
		add_link_options(LINKER:--rpath-link,/path/to/rootfs/lib)
		```

	c. Configure using cmake in a new directory build

		```
		$ export CMAKE_TOOLCHAIN_FILE=/path/to/cross_compile.cmake
		$ export PKG_CONFIG_ALLOW_SYSTEM_LIBS=FALSE
		$ export PKG_CONFIG_SYSROOT_DIR=/path/to/rootfs
		$ export PKG_CONFIG_LIBDIR=/path/to/rootfs/usr/lib/pkgconfig
		$ export PKG_CONFIG_PATH=
		$ mkdir -p build
		$ cd build
		$ cmake \
			-DCMAKE_INSTALL_PREFIX=/usr \
			-DCMAKE_PREFIX_PATH=/path/to/rootfs \
			-DOPENSSL_ROOT_DIR=/path/to/rootfs/usr \
			-DFLB_LIBYAML_DIR=/path/to/rootfs/usr \
			$OPT \
			/path/to/source/fluent-bit-4.2.2
		```

		The contents of cross_compile.cmake are as follows

		```
		set(CMAKE_SYSTEM_NAME Linux)
		set(CMAKE_C_COMPILER /path/to/cross-compiler/bin/armv6-rpi-linux-gnueabihf-gcc)
		set(CMAKE_CXX_COMPILER /path/to/cross-compiler/bin/armv6-rpi-linux-gnueabihf-g++)
		set(CMAKE_BUILD_RPATH "/path/to/rootfs")
		set(CMAKE_FIND_ROOT_PATH "/path/to/rootfs")
		set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
		set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
		set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
		```

	d. Run make in the build directory

		```
		$ cd build
		$ make -j20
		```

2. Copy the executable to the Raspberry Pi
3. Create a configuration file

	```
	service:
	   flush: 1
	   daemon: off
	   log_file: stderr
	   log_level: info
	   http_server: false

	pipeline:
	   inputs:
	      -  name: node_exporter_metrics
	         tag: metrics
	         metrics: "filesystem"
	         scrape_interval: 5
	   outputs:
	      -  name: stdout
	         match: metrics
	         format: json
	```

4. Run Fluent Bit

	```
	$ ./fluent-bit-4.2.2 -c config.yaml 2>/dev/null | grep 'mountpoint="/"'

	2026-02-06T17:09:01.531456231Z node_filesystem_avail_bytes{device="/dev/root",fstype="ext4",mountpoint="/"} = 2086236160
	2026-02-06T17:09:01.531456231Z node_filesystem_device_error{device="/dev/root",fstype="ext4",mountpoint="/"} = 0
	2026-02-06T17:09:01.531456231Z node_filesystem_files{device="/dev/root",fstype="ext4",mountpoint="/"} = 838832
	2026-02-06T17:09:01.531456231Z node_filesystem_files_free{device="/dev/root",fstype="ext4",mountpoint="/"} = 770647
	2026-02-06T17:09:01.531456231Z node_filesystem_free_bytes{device="/dev/root",fstype="ext4",mountpoint="/"} = 2789199872
	2026-02-06T17:09:01.531456231Z node_filesystem_readonly{device="/dev/root",fstype="ext4",mountpoint="/"} = 0
	2026-02-06T17:09:01.531456231Z node_filesystem_size_bytes{device="/dev/root",fstype="ext4",mountpoint="/"} = 556085248
	```

**Expected behavior**

I would expect node_filesystem_avail_bytes and node_filesystem_free_bytes to both be less than node_filesystem_size_bytes.

**Your Environment**

* Version used: 4.2.2
* Server type and version: Raspberry Pi 3 Model B Rev 1.2
* Operating System and version: Slackware 14.2 (32 bit)

**Additional context**

The cause appears to be an overflow issue. The following program reproduces the bug (when FIXED is not defined). This occurs when compiling the program directly on the Raspberry Pi.

```
#include <stdio.h>
#include <sys/statfs.h>

static int
test_value(char *name, long int bs, long int bn, double val)
{
	printf("%-32s = %6ld * %10ld = %15.0f\n", name, bs, bn, val);
}

#ifdef FIXED
#	define SIZE_CALC(_block_size, _blocks) ((long long int)(_block_size))*((long long int)(_blocks))
#else
#	define SIZE_CALC(_block_size, _blocks) _block_size * _blocks
#endif

int
main(int argc, char **argv)
{
	char *fs_path = "/";
	int result;
	struct statfs mount_point_info;

	printf("size of %-24s = %6ld\n", "int", sizeof(int));
	printf("size of %-24s = %6ld\n", "long int", sizeof(long int));
	printf("size of %-24s = %6ld\n", "long long int", sizeof(long long int));
	printf("size of %-24s = %6ld\n", "f_bsize", sizeof(mount_point_info.f_bsize));
	printf("size of %-24s = %6ld\n", "f_bavail", sizeof(mount_point_info.f_bavail));
	printf("size of %-24s = %6ld\n", "f_blocks", sizeof(mount_point_info.f_blocks));

	result = statfs(fs_path, &mount_point_info);
	if (result == 0) {
		test_value("node_filesystem_avail_bytes",
		           mount_point_info.f_bsize,
		           mount_point_info.f_bavail,
		           SIZE_CALC(mount_point_info.f_bsize, mount_point_info.f_bavail));
		test_value("node_filesystem_size_bytes",
		           mount_point_info.f_bsize,
		           mount_point_info.f_blocks,
		           SIZE_CALC(mount_point_info.f_bsize, mount_point_info.f_blocks));
	} else {
		printf("stat of %s failed\n", fs_path);
	}

	return 0;
}
```

Compile and run the example without the fix.

```
$ gcc -o example example.c
$ ./example 
size of int                      =      4
size of long int                 =      4
size of long long int            =      8
size of f_bsize                  =      4
size of f_bavail                 =      4
size of f_blocks                 =      4
node_filesystem_avail_bytes      =   4096 *    2606488 =      2086240256
node_filesystem_size_bytes       =   4096 *    3281491 =       556085248
```

Considering node_filesystem_avail_bytes, 4096 * 2,606,488 is 10,676,174,848 not 2,086,240,256. On the 32-bit system, the fields of the struct statfs are 32-bits, so multiplying them directly overflows. (10,676,174,848 mod 2^32 = 2,086,240,256). This is the same operation used in the Fluent Bit node_exporter input plugin. 

```
// From fluent-bit-4.2.2/plugins/in_node_exporter_metrics/ne_filesystem_linux.c, starting at line 227

                        cmt_gauge_set(ctx->fs_avail_bytes,
                                      timestamp,
                                      mount_point_info.f_bsize *
                                      mount_point_info.f_bavail,
                                      3, labels);
```

Compile and run the example with the fix.

```
$ gcc -o example example.c -DFIXED
$ ./example 
size of int                      =      4
size of long int                 =      4
size of long long int            =      8
size of f_bsize                  =      4
size of f_bavail                 =      4
size of f_blocks                 =      4
node_filesystem_avail_bytes      =   4096 *    2606487 =     10676170752
node_filesystem_size_bytes       =   4096 *    3281491 =     13440987136
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d6e65fb019a28ec2b16221e2753d4e3284e06ad0`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "fluent_fluent_bit__11435__d6e65fb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.

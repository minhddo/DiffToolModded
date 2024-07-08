# A Tree-Sitter - Gumtree Differentiation Co-package
This project is dedicated to get tree-sitter parser to work with gumtree conveniently by python interface with help of networkx.


## Running
### Download Jars file
[Download the `jars.zip` and unzip into `jars` folder](https://drive.google.com/file/d/18m3fhSdxhCuAS2aZuUROo2QLMSneuEcP/view?usp=sharing)
### Clone and Init submodules
```bash
git clone https://github.com/datvo06/tree-sitter-gumtree
git submodule update --init --recursive
```


### Install requirements
```bash
pip install tree-sitter
pip install networkx
```
### Example
#### Get map by line
Given 2 files as follows:
```cpp
// File 1
#include <stdio.h>

int main(int argc, char** argv){
		int a = 2;
		int b = 3;
		a = a + b;
		for (int i = 0; i < 3; i++){
				a += 1;
		}
		printf("Hello, World! %d\n", a);
		return 0;
}
```

and

```cpp
// File 2
#include <stdio.h>

int main(int argc, char** argv){
		int a = 2;
		int b = 3;
		b = a + b;
		int c = a - b;
		for (int i = 0; i < 3; i++){
				a += 1;
		}
		printf("Hello, World! %d\n", a);
		return 0;
}
```


```bash
python3 get_mapping_by_line <file1> <file2> <out_file>
python3 get_mapping_by_line selfunittests/file1.cpp selfunittests/file2.cpp out.json
```
This will give you the following results:
```json
{
    "mapping": {
        "1": 1,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 8,
        "8": 9,
        "9": 10,
        "10": 11,
        "11": 12,
        "12": 13
    },
    "deleted": [],
    "inserted": [
        7
    ]
}
```

Note that the empty lines are removed.

#### Interfacing and usage
The self unit test scripts can be found in `selfunittests/test_parse', and ran by
```bash
python -m selfunittests.test_parse
```

## Additional Info
## Json object format for communicating between jars file
(In case we wish to use the jar alone)
### Single json dict for description of an AST Tree:
- The input to `ast_diff.jar`  is as follows:
```json
"file1":{
	"nodes" {
		{
			"1": {
				"ntype": "identifier",
				"token": "a",
				"start_line": 1,
				"start_col": 1,
				"start_pos": 1,
				"end_line": 1,
				"end_col": 1,
				"end_pos": 1,
				"parent": -1
			},
			"size": 1
		}
	},
"file2": {
	...
}
}
```
and it will output the following
```json
{
	"srcNodes":{
			{
				"id": 0,
				"parent_id": -1,
				"type": "MethodCallExpr",
				"label": "nodeToJson",
				"range": {
					begin: {
						"pos": 0,
						"line": 1,
						"col": 0
					}
					end: {
						"pos": 6022,
						"line": 195
						"col": -1
				}
			}
		},
	},
	"dstNodes":{
	 ...
	},
	"mapping":{
		"1" : 1, // Id mapping
		...
	},
	"inserted": {
		2, 3, 4...
	},
	"deleted": {
		0
	}
}
```

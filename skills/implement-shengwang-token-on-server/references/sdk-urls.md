# AgoraDynamicKey SDK URLs

All implementations are in the same GitHub repo: https://github.com/AgoraIO/Tools

## Full Repo (recommended — download once, use any language)

```
https://github.com/AgoraIO/Tools
```

After downloading, find your language under:
```
Tools/DynamicKey/AgoraDynamicKey/<language>/src/
```

## Per-Language Paths (after download)

| Language | Source path | Sample |
|----------|-------------|--------|
| Go | `DynamicKey/AgoraDynamicKey/go/src/rtctokenbuilder2/` | `sample/RtcTokenBuilder2Sample.go` |
| Java | `DynamicKey/AgoraDynamicKey/java/src/main/java/io/agora/media/` | `RtcTokenBuilder2Sample.java` |
| Python | `DynamicKey/AgoraDynamicKey/python/src/RtcTokenBuilder2.py` | `sample/RtcTokenBuilder2Sample.py` |
| Python3 | `DynamicKey/AgoraDynamicKey/python3/src/RtcTokenBuilder2.py` | `sample/RtcTokenBuilder2Sample.py` |
| Node.js | `DynamicKey/AgoraDynamicKey/nodejs/src/RtcTokenBuilder2.js` | `sample/RtcTokenBuilder2Sample.js` |
| PHP | `DynamicKey/AgoraDynamicKey/php/src/RtcTokenBuilder2.php` | `sample/RtcTokenBuilder2Sample.php` |
| C++ | `DynamicKey/AgoraDynamicKey/cpp/src/RtcTokenBuilder2.h` | `sample/RtcTokenBuilder2Sample.cpp` |

## Go Module (direct import)

For Go projects, import directly without downloading:

```go
// go.mod
require github.com/AgoraIO/Tools v0.0.0  // check latest tag

// or copy the source files directly into your project
```

Note: The Tools repo is not a Go module — copy the `rtctokenbuilder2` source files into your project.

# SITO v0 pt 1 - The Base Stream

**tl;dr** - The Sito Base Stream is the outermost bytestream format carrying Sito pages. It comprises a sequence of Messagepack objects, containing metadata, substreams, etc. Messagepack does most of the heavy lifting. 

## The gist

- An L0 stream shall start with the 8-byte Sito magic byte sequence (SMBS) `92 3X 95 53 49 54 4f YY` (`'\x920\x95SITO\xYY'`), which corresponds to the object `[0x3X, [0x53, 0x49, 0x54, 0x4f, 0xYY]]`
- The page header byte `0x3X` (`0x30 <= 0x3x < 0x3A`) is always `0x30` for the first SMBS in a stream. `0x31` should be used for established streams (e.g. seek landing points). 
- YY is a Sito flags/version, nominally 0, semantics currently reserved
- Whenever possible, encoders should emit the SMBS on an 8-byte aligned boundary
- Encoders may emit any number of zero byte (`0x00`, preferred) or nil (`0xc0`) into the base stream between pages
- SMBS may be emitted at any point in the base stream. It can be frequent or not used at all, depending on application. 
- The base stream comprises a sequence of Messagepack formatted objects (pages)
- Actual Sito pages are tuples of `(page_head, [header], [payload], ...)` (see Sito pt2 - Pages)
- Maps in the base stream are reserved at this time (this may be used as explicitly labeled pages in the future)
- Primitives (e.g. nil, int, string, timestamp, ext, anything other than arrays/maps) in the base stream are "Comment Objects" and have no Sito v0 semantics. They can be ignored. They may be used for educational purposes, meta-annotation, testing, etc. 
- These may be used as comments or metadata, however decoders provide zero guarantees whether these objects will be decoded/propagated. Decoders MUST NOT rely on comment objects for decoding or out-of-band signalling. Use pages for these purposes; Sito pages are highly extensible. 
- The base stream may contain timestamp objects (always presumed to be UTC), which may be used to mark key timestamps in the event stream. These are merely optional metadata and must not be used for synchronization




```
In Messagepack spec notation, the start of a sito base stream looks like: 

+--------+--------+--------+--------+
|  0x92  |  0x30  |  0x95  |  0x53  |
+--------+--------+--------+--------+
+--------+--------+--------+--------+
|  0x49  |  0x54  |  0x4f  |  0x00  |
+--------+--------+--------+--------+
+~~~~~~~~+~~~~~~~~+~~~~~~~~+~~~~~~~~+
| object1| object2| object3| etc....|
+~~~~~~~~+~~~~~~~~+~~~~~~~~+~~~~~~~~+
```

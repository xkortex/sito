# Sito pt 2 - Pages

**tl;dr** - Pages are the prinicple building blocks of the Sito format. A Sito stream is simply a stream of pages, e
ach page being a Messagepack object. 

## Basic pages 

A basic page is a Messagepack fixarray/tuple. Different array lengths have different semantics. 
Zero-length arrays (`0x90`) are no-op and can be ignored. 

1. `(page_head,)` - A single PageHead object. Len-1 arrays are mostly used for control and no-ops
2. `(page_head, payload)` - A single object to express a payload, header, or metadata (depending on type)
3. `(page_head, header, payload)` - A payload with a formal header object. The header may be `nil`
4. `(page_head, header, payload, checksum)` - A checksummed or error-correcting-code page
5. `fixarray 5-15` - Currently unspecified, reserved

Every sub-element of a page is also Messagepack a object.

### PageHead

The first object within a page is always the PageHead (PH) object. PageHead may be a mapping, array, integer, string, though int is most typical. 
The object type of the PageHead may also convey information about the payload. Generally, decoders should be permissive about receiving unrecognized types.

### Formal Header

This is always a metadata object about the page. It may be `nil`. 


### Stateless and Stateful pages

A page is stateless if all information needed to fully decode and evaluate the current page is present is in page.
It is always possible to decode pages independently, but the semantics of a stateful page may not be defined 
unless the stream is first initialized.
If the page references prior pages, that page is considered stateful. 
The stream itself has a stream state, which is manipulated by pages. 

The `page_header` integer determines whether a page is definitely stateless or possibly stateful. 
Thus, the "first" bit of the page (the highest-order bit of the first byte) can be used to determine stateless pages. 
A zero in this position (`0b0xxxxxxx`) indicates a Sito PageHead type in the range 0-127, 
which is guaranteed to be stateless. 
A one in this position (`0b1xxxxxxx`, aka all other Msgpack objects) indicate that the stream *may* be stateful 
(but is allowed to be stateless). 

### The Sito control stream 

Pages of the form `(0b0xxxxxxx, payload, ...)` are stream control pages (SCP). 
These pages are always stateless in themselves (they may not refer to prior data), but are used to provide metadata and 
manipulate the stream state (which is of course stateful). For example, `0x01` is an INFO page. 
(See [Stream Control Pages](./sito_pt3_state_control.md)) 

## PageHead Types overview

### No-op pages (0x00, 0x90, 0xc0-0xc2)

Pages with a header of zero, nil, zero-array `()`/`0x90`, `0xc1`, or `false`, are no-ops. Decoders should ignore any payload associated with a no-op header. Encoders are allowed to write a zero-array `0x90` or zero-page (header=0 with some payload), but these must be ignored by a decoder. `true`/`0xc3` is undefined and should be ignored. Writing a header of `0xc0-0xc3` is reserved. 


### Fixint Integer headers (0x01 - 0x7f, 0xe0 - 0xff)

Headers that are integers have pre-defined meanings. Positive fixints (1 to 127) have reserved meanings in Sito. can be used freely to pad the stream, which makes it a no-op (and ergo stateless). Negative fixints (-32 to -1) have specific semantics (to be defined - one option is that they refer to specific streams, and are simply a shorthand for integer headers, `stream_number = -1 - header_int` (See integer headers).)



### Integer PH headers  (uint 8/16/32/64)

Pages with integer headers are always stateful - they must refer to pre-defined streams. `0` is Stream 0, `1` is Stream 1, etc. Signed integer headers are currently reserved. 


### String PH headers (Plain path)

Pages with string header objects refer to "plain path" objects - blobs of data with UTF-8 identifiers/paths. 

### Fixext (1/2/4/8/16) headers

Fixext headers up to 16 bytes are reserved. Fixext *payloads* may be used by the application.

### Ext PH headers

Ext headers >16 bytes with codes >64 (`0x40-0x7f`) may be used by the application, but only if registered in the stream (which is currently undefined, so effectively this is reserved). Codes <64 are reserved. 
    
    
### Other PH headers

All other header types are reserved. 



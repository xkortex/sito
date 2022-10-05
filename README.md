# Sito Container Format 

**tl;dr** - a modern container format, based on [messagepack](https://msgpack.org/index.html), 
which is easy to reason about, implement, hack on, and use.
The sito format is platform independent, parallel, multiplexed, chunkable, seekable, indexable, 
and able to be distributed. It excels at temporal/stream data, but also works great for static storage and archiving. 

#### Name 

The name "Sito" refers to cereal/grain, by way of *σῑτό- (*sītó-, “threshed”), derived from Proto-Indo-European 
*tih₂-tó- (“struck”). I have also seen it as an alternate name/title for Ceres, 
the goddess of agriculture. It's a pun on serialization -> cerealization. 
It's also a backcronym for Standard Interface for Transporting Objects. 

### The format

The sito format comprises a collection of pages - "data boxes" - in a 
[linear sequence or stream](./docs/sito_pt1_stream.md). Each page
is an independently-decodable msgpack fixed-array object. Messagepack is an object serialization
specification and does the heavy lifting of converting in-memory data types into bytes, 
and vice-versa. 

[Pages](./docs/sito_pt2_pages.md) are organized into orthogonal substreams. 
Substreams can be multiplexed into a single logical byte stream, or de-interleaved into separate streams.
Pages are the primary unit of data storage, and are always 
a [fixarray](https://github.com/msgpack/msgpack/blob/master/spec.md#array-format-family) 
of 1-15 objects of the form `(page_head: int, [header: map, [payload: Any, ...]])`. 
The simplest page is the zero page `(0,)` (no-op), and up to 15 fields are allowed.  


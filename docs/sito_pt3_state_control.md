# Sito pt 3 - State Control

**tl;dr** - Sito state is modeled after Event Sourcing. 
The stream state exists as an abstract object, and control pages are used to manipulate that state. 
State is essentially a (K, T, V) structure, key/time/value triples, time in the abstract sense. 

### Control pages

Control pages are what manipulate state. 

## Sito PageHead types

(very much work-in-progress)

The semantics of control pages are inspired in part by ASCII control codes. 

- `0x00` ZERO - The zero page. Treated as a no-op
- `0x01` INFO - Non-binding information 
- `0x02` STS  - Start of (sub)stream 
- `0x03` ETS  - End of (sub)stream
- `0x04` EOT  - End of transmission 
- `0x05` SET  - Set parameter(s) value(s)
- `0x08` DEL  - Delete parameter(s)
- `0x16` SYNC - Used for stream re-synchronization
- `0x30 <= 0x3x < 0x3A` SMBS - Used as part of sito magic byte sequence

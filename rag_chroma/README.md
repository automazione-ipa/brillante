### VC 2019 e python==3.11.9

Installing "Microsoft Visual C++ 14.0 or greater" components is a bit of an overkill for me, ~4GB to download :-/
It should be a workaround rather than the solution, so I end up with another workaround.

I have Windows 10 Pro (10.0.19045) with two redistributables installed:

MSVC 2015-2022 Redistributable (x64) - 14.42.34433.0
MSVC 2015-2022 Redistributable (x86) - 14.42.34433.0
Tried simple pip install chromadb with Python 3.13.1, 3.12.8 and it didn't work.
Finally it clicked with Python 3.11.9, but at the moment I cannot deduce why only this one.

- - -

### Soluzione C

pip install chromadb==0.5.0 chroma-hnswlib==0.7.3


https://github.com/chroma-core/chroma/issues/189#issuecomment-1454418844
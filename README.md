# Font App
App for determine fonts on image

## Algorithms
- First algorithm is a cosine distance of vectors. Every image from database stored as a vector stored as a vector obtained using an encoder from the library img2vec-pytorch. If necessary, they are restored from vectors using a decoder
- Second algorithm compares the images recovered from the vectors with the image from which the font needs to be determined
- Third algorithm compares image hashes

## Future plans
- Developing the ability to identify a font from an image with a word, not a letter.
- Adding other languages for font recognition by image

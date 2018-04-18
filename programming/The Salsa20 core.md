# The Salsa20 core

# Salsa20 核函数

The Salsa20 core is a function from 64-byte strings to 64-byte strings: the Salsa20 core reads a 64-byte string x and produces a 64-byte string Salsa20(x).

Salsa20核函数将一个64字节的字节流x转换为另一个64字节的字节流Salsa20(x)，这个函数的产生的伪随机字节流主要用来对消息进行异或操作达到加密的效果。

The [Salsa20 stream cipher](https://cr.yp.to/snuffle.html) has a separate page. The Salsa20 stream cipher uses the Salsa20 core to encrypt data.

[Salsa20 流加密算法](https://cr.yp.to/snuffle.html)有一个专门的网页。Salsa20 流加密算法使用Salsa20核来加密数据。

The [Rumba20 compression function](https://cr.yp.to/rumba20.html) has a separate page. The Rumba20 compression function uses the Salsa20 core to compress a 192-byte string to a 64-byte string.

[Rumba20压缩函数](https://cr.yp.to/rumba20.html)有一个独立的网页。Rumba20压缩函数使用Salsa20核将192字节数据压缩为64字节。

I originally introduced the Salsa20 core as the "Salsa20 hash function," but this terminology turns out to confuse people who think that "hash function" means "collision-resistant compression function." The Salsa20 core does not compress and is not collision-resistant. If you want a collision-resistant compression function, look at Rumba20. (I wonder what the same people think of the FNV hash function, perfect hash functions, universal hash functions, etc.)

我最开始使用Salsa20哈希函数来命名Salsa20核函数，但是这个专业的叫法让人们误认为这个哈希函数是collision-resistant的。（collision-resistant指两个不同的输入值传入这个哈希函数后，必然不会产生相同的输出值，这个哈希函数就是collision-resistant）Salsa20核函数并不压缩数据和collision-resistant。如果你需要满足这样条件的哈希函数请参考Rumba20。

History: I introduced Salsa20 in March 2005. It is a refinement of [Salsa10](https://cr.yp.to/salsa10.html), which I introduced in November 2004.

历史：我在2005年3月引入了Salsa20。它对我在2004年11月提出的 [Salsa10](https://cr.yp.to/salsa10.html)进行了改良。

ChaCha20在核函数上稍微做了调整，数据bit扩散更快。每一个1/4 round会修改一个字两次，每一个输入字也会影响到输出字。

## Definition of the Salsa20 core

## Salsa20核函数的定义

The 64-byte input x to Salsa20 is viewed in little-endian form as 16 words x0, x1, x2, ..., x15 in {0,1,...,2^32-1}. These 16 words are fed through 320 invertible modifications, where each modification changes one word. The resulting 16 words are added to the original x0, x1, x2, ..., x15 respectively modulo 2^32, producing, in little-endian form, the 64-byte output Salsa20(x).

将64字节的输入流x看作16个字 x0, x1, x2, ..., x15，其中每个字为4个字节的小端对齐的无符号数字。由于字只有4个字节，因此字的范围在{0,1,...,2^32-1}中。对这16个字进行总计320次可翻转的转换得到输出的16个字。最后将输出的16个字分别加上原来的16个字并对2的32次方取模，同样保持小端字节序，从而得到64字节的输出字节流Salsa20(x).

Each modification involves xor'ing into one word a rotated version of the sum of two other words modulo 2^32. Thus the 320 modifications involve, overall, 320 additions, 320 xor's, and 320 rotations. The rotations are all by constant distances.

每一个转换改变一个字z，先将两个其他的字x和y加和取2的32次方的模，再循环移位固定的距离后，将这个结果和z进行异或操作得到新的z。循环移位的距离是固定的。因此320次转换总的计算量包括320次加法、320次异或、320次循环移位操作。

The entire series of modifications is a series of 10 identical double-rounds. Each double-round is a series of 2 rounds. Each round is a set of 4 parallel quarter-rounds. Each quarter-round modifies 4 words.

整个转换过程包含10次相同的 double-round。每一个双倍循环又由两个rounds组成.每一个round由4个并行的1/4的round组成。每一个1/4的round转换4个字。

The complete function is defined as follows:

完整的函数定义如下：

```c
b ^= (a+d) <<< 7;
c ^= (b+a) <<< 9;
d ^= (c+b) <<< 13;
a ^= (d+c) <<< 18;	
// R(a,b)宏定义了一个简单的循环左移位操作，rotl32(),C语言没有实现这个操作，汇编语言实现了
     #define R(a,b) (((a) << (b)) | ((a) >> (32 - (b))))
     void salsa20_word_specification(uint32 out[16],uint32 in[16])
     {
       int i;
       uint32 x[16];
       for (i = 0;i < 16;++i) x[i] = in[i];
       // 这个循环10次
       for (i = 20;i > 0;i -= 2) {
       // 循环移位的距离总是7,9,13,18，每4个语句为一组，例如前4个只对4,8,12,0进行转换
         x[ 4] ^= R(x[ 0]+x[12], 7);  x[ 8] ^= R(x[ 4]+x[ 0], 9);
         x[12] ^= R(x[ 8]+x[ 4],13);  x[ 0] ^= R(x[12]+x[ 8],18);
         x[ 9] ^= R(x[ 5]+x[ 1], 7);  x[13] ^= R(x[ 9]+x[ 5], 9);
         x[ 1] ^= R(x[13]+x[ 9],13);  x[ 5] ^= R(x[ 1]+x[13],18);
         x[14] ^= R(x[10]+x[ 6], 7);  x[ 2] ^= R(x[14]+x[10], 9);
         x[ 6] ^= R(x[ 2]+x[14],13);  x[10] ^= R(x[ 6]+x[ 2],18);
         x[ 3] ^= R(x[15]+x[11], 7);  x[ 7] ^= R(x[ 3]+x[15], 9);
         x[11] ^= R(x[ 7]+x[ 3],13);  x[15] ^= R(x[11]+x[ 7],18);
         x[ 1] ^= R(x[ 0]+x[ 3], 7);  x[ 2] ^= R(x[ 1]+x[ 0], 9);
         x[ 3] ^= R(x[ 2]+x[ 1],13);  x[ 0] ^= R(x[ 3]+x[ 2],18);
         x[ 6] ^= R(x[ 5]+x[ 4], 7);  x[ 7] ^= R(x[ 6]+x[ 5], 9);
         x[ 4] ^= R(x[ 7]+x[ 6],13);  x[ 5] ^= R(x[ 4]+x[ 7],18);
         x[11] ^= R(x[10]+x[ 9], 7);  x[ 8] ^= R(x[11]+x[10], 9);
         x[ 9] ^= R(x[ 8]+x[11],13);  x[10] ^= R(x[ 9]+x[ 8],18);
         x[12] ^= R(x[15]+x[14], 7);  x[13] ^= R(x[12]+x[15], 9);
         x[14] ^= R(x[13]+x[12],13);  x[15] ^= R(x[14]+x[13],18);
       }
       // 最后转换后的字与原始字进行加和
       for (i = 0;i < 16;++i) out[i] = x[i] + in[i];
     }
```

Here `in` is the sequence of input words, and `out` is the sequence of output words. The caller handles any necessary endianness conversion and alignment.

其中`in`是输入的16个字，`out`时输出的16个字，调用者需要处理必要的大小端转换和字节对齐。

CHACHA的核函数

Obviously the ChaCha quarter-round, unlike the Salsa20 quarter-round, gives each input word a chance to affect each output word. Less obvious is that the ChaCha quarter-round diffuses changes through bits more quickly than the Salsa20 quarter-round. One can see this by tracing every possible 1-bit input difference: in the absence of carries, the ChaCha quarter-round changes (on average) 12.5 output bits, while the Salsa20 quarter-round changes 8 output bits.

```C
a += b; d ^= a; d <<<= 16;
c += d; b ^= c; b <<<= 12;
a += b; d ^= a; d <<<= 8;
c += d; b ^= c; b <<<= 7;

#define QUARTERROUND(a,b,c,d) \
  x[a] = PLUS(x[a],x[b]); x[d] = ROTATE(XOR(x[d],x[a]),16); \
  x[c] = PLUS(x[c],x[d]); x[b] = ROTATE(XOR(x[b],x[c]),12); \
  x[a] = PLUS(x[a],x[b]); x[d] = ROTATE(XOR(x[d],x[a]), 8); \
  x[c] = PLUS(x[c],x[d]); x[b] = ROTATE(XOR(x[b],x[c]), 7);

static void salsa20_wordtobyte(u8 output[64],const u32 input[16])
{
  u32 x[16];
  int i;

  for (i = 0;i < 16;++i) x[i] = input[i];
  for (i = 8;i > 0;i -= 2) {
    QUARTERROUND( 0, 4, 8,12)
    QUARTERROUND( 1, 5, 9,13)
    QUARTERROUND( 2, 6,10,14)
    QUARTERROUND( 3, 7,11,15)
    QUARTERROUND( 0, 5,10,15)
    QUARTERROUND( 1, 6,11,12)
    QUARTERROUND( 2, 7, 8,13)
    QUARTERROUND( 3, 4, 9,14)
  }
  for (i = 0;i < 16;++i) x[i] = PLUS(x[i],input[i]);
  for (i = 0;i < 16;++i) U32TO8_LITTLE(output + 4 * i,x[i]);
}
```



一个具体实现的例子[salsa20.c](https://cr.yp.to/snuffle/salsa20/ref/salsa20.c)

```C
/*
salsa20-ref.c version 20051118
D. J. Bernstein
Public domain.
*/

#include "ecrypt-sync.h"

#define ROTATE(v,c) (ROTL32(v,c))
#define XOR(v,w) ((v) ^ (w))
#define PLUS(v,w) (U32V((v) + (w)))
#define PLUSONE(v) (PLUS((v),1))

static void salsa20_wordtobyte(u8 output[64],const u32 input[16])
{
  u32 x[16];
  int i;

  for (i = 0;i < 16;++i) x[i] = input[i];
  for (i = 20;i > 0;i -= 2) {
    x[ 4] = XOR(x[ 4],ROTATE(PLUS(x[ 0],x[12]), 7));
    x[ 8] = XOR(x[ 8],ROTATE(PLUS(x[ 4],x[ 0]), 9));
    x[12] = XOR(x[12],ROTATE(PLUS(x[ 8],x[ 4]),13));
    x[ 0] = XOR(x[ 0],ROTATE(PLUS(x[12],x[ 8]),18));
    x[ 9] = XOR(x[ 9],ROTATE(PLUS(x[ 5],x[ 1]), 7));
    x[13] = XOR(x[13],ROTATE(PLUS(x[ 9],x[ 5]), 9));
    x[ 1] = XOR(x[ 1],ROTATE(PLUS(x[13],x[ 9]),13));
    x[ 5] = XOR(x[ 5],ROTATE(PLUS(x[ 1],x[13]),18));
    x[14] = XOR(x[14],ROTATE(PLUS(x[10],x[ 6]), 7));
    x[ 2] = XOR(x[ 2],ROTATE(PLUS(x[14],x[10]), 9));
    x[ 6] = XOR(x[ 6],ROTATE(PLUS(x[ 2],x[14]),13));
    x[10] = XOR(x[10],ROTATE(PLUS(x[ 6],x[ 2]),18));
    x[ 3] = XOR(x[ 3],ROTATE(PLUS(x[15],x[11]), 7));
    x[ 7] = XOR(x[ 7],ROTATE(PLUS(x[ 3],x[15]), 9));
    x[11] = XOR(x[11],ROTATE(PLUS(x[ 7],x[ 3]),13));
    x[15] = XOR(x[15],ROTATE(PLUS(x[11],x[ 7]),18));
    x[ 1] = XOR(x[ 1],ROTATE(PLUS(x[ 0],x[ 3]), 7));
    x[ 2] = XOR(x[ 2],ROTATE(PLUS(x[ 1],x[ 0]), 9));
    x[ 3] = XOR(x[ 3],ROTATE(PLUS(x[ 2],x[ 1]),13));
    x[ 0] = XOR(x[ 0],ROTATE(PLUS(x[ 3],x[ 2]),18));
    x[ 6] = XOR(x[ 6],ROTATE(PLUS(x[ 5],x[ 4]), 7));
    x[ 7] = XOR(x[ 7],ROTATE(PLUS(x[ 6],x[ 5]), 9));
    x[ 4] = XOR(x[ 4],ROTATE(PLUS(x[ 7],x[ 6]),13));
    x[ 5] = XOR(x[ 5],ROTATE(PLUS(x[ 4],x[ 7]),18));
    x[11] = XOR(x[11],ROTATE(PLUS(x[10],x[ 9]), 7));
    x[ 8] = XOR(x[ 8],ROTATE(PLUS(x[11],x[10]), 9));
    x[ 9] = XOR(x[ 9],ROTATE(PLUS(x[ 8],x[11]),13));
    x[10] = XOR(x[10],ROTATE(PLUS(x[ 9],x[ 8]),18));
    x[12] = XOR(x[12],ROTATE(PLUS(x[15],x[14]), 7));
    x[13] = XOR(x[13],ROTATE(PLUS(x[12],x[15]), 9));
    x[14] = XOR(x[14],ROTATE(PLUS(x[13],x[12]),13));
    x[15] = XOR(x[15],ROTATE(PLUS(x[14],x[13]),18));
  }
  for (i = 0;i < 16;++i) x[i] = PLUS(x[i],input[i]);
  for (i = 0;i < 16;++i) U32TO8_LITTLE(output + 4 * i,x[i]);
}

void ECRYPT_init(void)
{
  return;
}

static const char sigma[16] = "expand 32-byte k";
static const char tau[16] = "expand 16-byte k";

#define U8TO32_LITTLE(p) \
  (((u32)((p)[0])      ) | \
   ((u32)((p)[1]) <<  8) | \
   ((u32)((p)[2]) << 16) | \
   ((u32)((p)[3]) << 24))
   
/*
 * Key setup. It is the user's responsibility to select the values of
 * keysize and ivsize from the set of supported values specified
 * above.
 */
void ECRYPT_keysetup(ECRYPT_ctx *x,const u8 *k,u32 kbits,u32 ivbits)
{
  const char *constants;

  x->input[1] = U8TO32_LITTLE(k + 0);
  x->input[2] = U8TO32_LITTLE(k + 4);
  x->input[3] = U8TO32_LITTLE(k + 8);
  x->input[4] = U8TO32_LITTLE(k + 12);
  if (kbits == 256) { /* recommended */
    k += 16;
    constants = sigma;
  } else { /* kbits == 128 */
    constants = tau;
  }
  x->input[11] = U8TO32_LITTLE(k + 0);
  x->input[12] = U8TO32_LITTLE(k + 4);
  x->input[13] = U8TO32_LITTLE(k + 8);
  x->input[14] = U8TO32_LITTLE(k + 12);
  x->input[0] = U8TO32_LITTLE(constants + 0);
  x->input[5] = U8TO32_LITTLE(constants + 4);
  x->input[10] = U8TO32_LITTLE(constants + 8);
  x->input[15] = U8TO32_LITTLE(constants + 12);
}
/*
 * IV setup. After having called ECRYPT_keysetup(), the user is
 * allowed to call ECRYPT_ivsetup() different times in order to
 * encrypt/decrypt different messages with the same key but different
 * IV's.
 */
void ECRYPT_ivsetup(ECRYPT_ctx *x,const u8 *iv)
{
  x->input[6] = U8TO32_LITTLE(iv + 0);
  x->input[7] = U8TO32_LITTLE(iv + 4);
  x->input[8] = 0;
  x->input[9] = 0;
}
// 加密数据流，m为消息，c为输出的密文，bytes为消息长度
void ECRYPT_encrypt_bytes(ECRYPT_ctx *x,const u8 *m,u8 *c,u32 bytes)
{
  u8 output[64];
  int i;

  if (!bytes) return;
  for (;;) {
  // 先使用核函数得到随机字节流
    salsa20_wordtobyte(output,x->input);
    // 得到一个新的nonce，nonce是一个加密术语，number once的缩写，标识每次加密使用的数字都是不同的，这里自动累加1
    x->input[8] = PLUSONE(x->input[8]);
    if (!x->input[8]) {
      x->input[9] = PLUSONE(x->input[9]);
      /* stopping at 2^70 bytes per nonce is user's responsibility */
    }
    if (bytes <= 64) {
    	// 如果字节流长度小于64,则让消息每一个字节和输出随机字节流一一异或
      for (i = 0;i < bytes;++i) c[i] = m[i] ^ output[i];
      return;
    }
    // 如果字节流长度大于64字节，一次循环只处理64个字节，加密下一组数据时重新计算output
    for (i = 0;i < 64;++i) c[i] = m[i] ^ output[i];
    bytes -= 64;
    c += 64;
    m += 64;
  }
}

void ECRYPT_decrypt_bytes(ECRYPT_ctx *x,const u8 *c,u8 *m,u32 bytes)
{
  ECRYPT_encrypt_bytes(x,c,m,bytes);
}

void ECRYPT_keystream_bytes(ECRYPT_ctx *x,u8 *stream,u32 bytes)
{
  u32 i;
  for (i = 0;i < bytes;++i) stream[i] = 0;
  ECRYPT_encrypt_bytes(x,stream,stream,bytes);
}
```

依赖的头文件实现[ecrypt-portable.h](https://cr.yp.to/snuffle/ecrypt-portable.h)
```C
/* ecrypt-portable.h */

/*
 * WARNING: the conversions defined below are implemented as macros,
 * and should be used carefully. They should NOT be used with
 * parameters which perform some action. E.g., the following two lines
 * are not equivalent:
 * 
 *  1) ++x; y = ROTL32(x, n); 
 *  2) y = ROTL32(++x, n);
 */

/*
 * *** Please do not edit this file. ***
 *
 * The default macros can be overridden for specific architectures by
 * editing 'ecrypt-machine.h'.
 */

#ifndef ECRYPT_PORTABLE
#define ECRYPT_PORTABLE

#include "ecrypt-config.h"

/* ------------------------------------------------------------------------- */

/*
 * The following types are defined (if available):
 *
 * u8:  unsigned integer type, at least 8 bits
 * u16: unsigned integer type, at least 16 bits
 * u32: unsigned integer type, at least 32 bits
 * u64: unsigned integer type, at least 64 bits
 *
 * s8, s16, s32, s64 -> signed counterparts of u8, u16, u32, u64
 *
 * The selection of minimum-width integer types is taken care of by
 * 'ecrypt-config.h'. Note: to enable 64-bit types on 32-bit
 * compilers, it might be necessary to switch from ISO C90 mode to ISO
 * C99 mode (e.g., gcc -std=c99).
 */

#ifdef I8T
typedef signed I8T s8;
typedef unsigned I8T u8;
#endif

#ifdef I16T
typedef signed I16T s16;
typedef unsigned I16T u16;
#endif

#ifdef I32T
typedef signed I32T s32;
typedef unsigned I32T u32;
#endif

#ifdef I64T
typedef signed I64T s64;
typedef unsigned I64T u64;
#endif

/*
 * The following macros are used to obtain exact-width results.
 */

#define U8V(v) ((u8)(v) & U8C(0xFF))
#define U16V(v) ((u16)(v) & U16C(0xFFFF))
#define U32V(v) ((u32)(v) & U32C(0xFFFFFFFF))
#define U64V(v) ((u64)(v) & U64C(0xFFFFFFFFFFFFFFFF))

/* ------------------------------------------------------------------------- */

/*
 * The following macros return words with their bits rotated over n
 * positions to the left/right.
 */

#define ECRYPT_DEFAULT_ROT

#define ROTL8(v, n) \
  (U8V((v) << (n)) | ((v) >> (8 - (n))))

#define ROTL16(v, n) \
  (U16V((v) << (n)) | ((v) >> (16 - (n))))

#define ROTL32(v, n) \
  (U32V((v) << (n)) | ((v) >> (32 - (n))))

#define ROTL64(v, n) \
  (U64V((v) << (n)) | ((v) >> (64 - (n))))

#define ROTR8(v, n) ROTL8(v, 8 - (n))
#define ROTR16(v, n) ROTL16(v, 16 - (n))
#define ROTR32(v, n) ROTL32(v, 32 - (n))
#define ROTR64(v, n) ROTL64(v, 64 - (n))

#include "ecrypt-machine.h"

/* ------------------------------------------------------------------------- */

/*
 * The following macros return a word with bytes in reverse order.
 */

#define ECRYPT_DEFAULT_SWAP

#define SWAP16(v) \
  ROTL16(v, 8)

#define SWAP32(v) \
  ((ROTL32(v,  8) & U32C(0x00FF00FF)) | \
   (ROTL32(v, 24) & U32C(0xFF00FF00)))

#ifdef ECRYPT_NATIVE64
#define SWAP64(v) \
  ((ROTL64(v,  8) & U64C(0x000000FF000000FF)) | \
   (ROTL64(v, 24) & U64C(0x0000FF000000FF00)) | \
   (ROTL64(v, 40) & U64C(0x00FF000000FF0000)) | \
   (ROTL64(v, 56) & U64C(0xFF000000FF000000)))
#else
#define SWAP64(v) \
  (((u64)SWAP32(U32V(v)) << 32) | (u64)SWAP32(U32V(v >> 32)))
#endif

#include "ecrypt-machine.h"

#define ECRYPT_DEFAULT_WTOW

#ifdef ECRYPT_LITTLE_ENDIAN
#define U16TO16_LITTLE(v) (v)
#define U32TO32_LITTLE(v) (v)
#define U64TO64_LITTLE(v) (v)

#define U16TO16_BIG(v) SWAP16(v)
#define U32TO32_BIG(v) SWAP32(v)
#define U64TO64_BIG(v) SWAP64(v)
#endif

#ifdef ECRYPT_BIG_ENDIAN
#define U16TO16_LITTLE(v) SWAP16(v)
#define U32TO32_LITTLE(v) SWAP32(v)
#define U64TO64_LITTLE(v) SWAP64(v)

#define U16TO16_BIG(v) (v)
#define U32TO32_BIG(v) (v)
#define U64TO64_BIG(v) (v)
#endif

#include "ecrypt-machine.h"

/*
 * The following macros load words from an array of bytes with
 * different types of endianness, and vice versa.
 */

#define ECRYPT_DEFAULT_BTOW

#if (!defined(ECRYPT_UNKNOWN) && defined(ECRYPT_I8T_IS_BYTE))

#define U8TO16_LITTLE(p) U16TO16_LITTLE(((u16*)(p))[0])
#define U8TO32_LITTLE(p) U32TO32_LITTLE(((u32*)(p))[0])
#define U8TO64_LITTLE(p) U64TO64_LITTLE(((u64*)(p))[0])

#define U8TO16_BIG(p) U16TO16_BIG(((u16*)(p))[0])
#define U8TO32_BIG(p) U32TO32_BIG(((u32*)(p))[0])
#define U8TO64_BIG(p) U64TO64_BIG(((u64*)(p))[0])

#define U16TO8_LITTLE(p, v) (((u16*)(p))[0] = U16TO16_LITTLE(v))
#define U32TO8_LITTLE(p, v) (((u32*)(p))[0] = U32TO32_LITTLE(v))
#define U64TO8_LITTLE(p, v) (((u64*)(p))[0] = U64TO64_LITTLE(v))

#define U16TO8_BIG(p, v) (((u16*)(p))[0] = U16TO16_BIG(v))
#define U32TO8_BIG(p, v) (((u32*)(p))[0] = U32TO32_BIG(v))
#define U64TO8_BIG(p, v) (((u64*)(p))[0] = U64TO64_BIG(v))

#else

#define U8TO16_LITTLE(p) \
  (((u16)((p)[0])      ) | \
   ((u16)((p)[1]) <<  8))

#define U8TO32_LITTLE(p) \
  (((u32)((p)[0])      ) | \
   ((u32)((p)[1]) <<  8) | \
   ((u32)((p)[2]) << 16) | \
   ((u32)((p)[3]) << 24))

#ifdef ECRYPT_NATIVE64
#define U8TO64_LITTLE(p) \
  (((u64)((p)[0])      ) | \
   ((u64)((p)[1]) <<  8) | \
   ((u64)((p)[2]) << 16) | \
   ((u64)((p)[3]) << 24) | \
   ((u64)((p)[4]) << 32) | \
   ((u64)((p)[5]) << 40) | \
   ((u64)((p)[6]) << 48) | \
   ((u64)((p)[7]) << 56))
#else
#define U8TO64_LITTLE(p) \
  ((u64)U8TO32_LITTLE(p) | ((u64)U8TO32_LITTLE((p) + 4) << 32))
#endif

#define U8TO16_BIG(p) \
  (((u16)((p)[0]) <<  8) | \
   ((u16)((p)[1])      ))

#define U8TO32_BIG(p) \
  (((u32)((p)[0]) << 24) | \
   ((u32)((p)[1]) << 16) | \
   ((u32)((p)[2]) <<  8) | \
   ((u32)((p)[3])      ))

#ifdef ECRYPT_NATIVE64
#define U8TO64_BIG(p) \
  (((u64)((p)[0]) << 56) | \
   ((u64)((p)[1]) << 48) | \
   ((u64)((p)[2]) << 40) | \
   ((u64)((p)[3]) << 32) | \
   ((u64)((p)[4]) << 24) | \
   ((u64)((p)[5]) << 16) | \
   ((u64)((p)[6]) <<  8) | \
   ((u64)((p)[7])      ))
#else
#define U8TO64_BIG(p) \
  (((u64)U8TO32_BIG(p) << 32) | (u64)U8TO32_BIG((p) + 4))
#endif

#define U16TO8_LITTLE(p, v) \
  do { \
    (p)[0] = U8V((v)      ); \
    (p)[1] = U8V((v) >>  8); \
  } while (0)

#define U32TO8_LITTLE(p, v) \
  do { \
    (p)[0] = U8V((v)      ); \
    (p)[1] = U8V((v) >>  8); \
    (p)[2] = U8V((v) >> 16); \
    (p)[3] = U8V((v) >> 24); \
  } while (0)

#ifdef ECRYPT_NATIVE64
#define U64TO8_LITTLE(p, v) \
  do { \
    (p)[0] = U8V((v)      ); \
    (p)[1] = U8V((v) >>  8); \
    (p)[2] = U8V((v) >> 16); \
    (p)[3] = U8V((v) >> 24); \
    (p)[4] = U8V((v) >> 32); \
    (p)[5] = U8V((v) >> 40); \
    (p)[6] = U8V((v) >> 48); \
    (p)[7] = U8V((v) >> 56); \
  } while (0)
#else
#define U64TO8_LITTLE(p, v) \
  do { \
    U32TO8_LITTLE((p),     U32V((v)      )); \
    U32TO8_LITTLE((p) + 4, U32V((v) >> 32)); \
  } while (0)
#endif

#define U16TO8_BIG(p, v) \
  do { \
    (p)[0] = U8V((v)      ); \
    (p)[1] = U8V((v) >>  8); \
  } while (0)

#define U32TO8_BIG(p, v) \
  do { \
    (p)[0] = U8V((v) >> 24); \
    (p)[1] = U8V((v) >> 16); \
    (p)[2] = U8V((v) >>  8); \
    (p)[3] = U8V((v)      ); \
  } while (0)

#ifdef ECRYPT_NATIVE64
#define U64TO8_BIG(p, v) \
  do { \
    (p)[0] = U8V((v) >> 56); \
    (p)[1] = U8V((v) >> 48); \
    (p)[2] = U8V((v) >> 40); \
    (p)[3] = U8V((v) >> 32); \
    (p)[4] = U8V((v) >> 24); \
    (p)[5] = U8V((v) >> 16); \
    (p)[6] = U8V((v) >>  8); \
    (p)[7] = U8V((v)      ); \
  } while (0)
#else
#define U64TO8_BIG(p, v) \
  do { \
    U32TO8_BIG((p),     U32V((v) >> 32)); \
    U32TO8_BIG((p) + 4, U32V((v)      )); \
  } while (0)
#endif

#endif

#include "ecrypt-machine.h"

/* ------------------------------------------------------------------------- */

#endif
```
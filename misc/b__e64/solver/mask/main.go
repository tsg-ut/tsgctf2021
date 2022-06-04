package main

import (
	"bytes"
	"context"
	"encoding/base64"
	"fmt"
	"math"
	"math/rand"
	"sort"
	"time"
)

const (
	plen           = 32
	elen           = 344
	mlen           = elen / 3
	itr            = 8
	cmask          = byte('*')
	defaultCharset = "abcdefghijklmnopqrstuvwxyz0123456789"
)

func enc(data []byte) []byte {
	for i := 0; i < itr; i++ {
		d := make([]byte, base64.StdEncoding.EncodedLen(len(data)))
		base64.StdEncoding.Encode(d, data)
		data = d
	}
	return data
}

func generateChallenge(charset []byte) []byte {
	plain := make([]byte, plen)
	for j := 0; j < plen; j++ {
		plain[j] = charset[rand.Intn(len(charset))]
	}
	return plain
}

func solve(ctx context.Context, encoded []byte, charset []byte) []byte {
	dr := make([]int, plen)
	for i := 0; i < plen; i++ {
		dr[i] = i + 1
		for j := 0; j < itr; j++ {
			dr[i] = dr[i] * 8 / 6
		}
	}
	dr[plen-1] = len(encoded)

	cur := 0
	idx := make([]int, plen)
	res := make([]byte, plen)
	for i := 0; i < plen; i++ {
		res[i] = charset[0]
	}

	for cur < plen {
		select {
		case <-ctx.Done():
			return nil
		default:
		}

		cipher := enc(res[:])
		ok := true
		for i := 0; i < dr[cur]; i++ {
			if encoded[i] != cmask && encoded[i] != cipher[i] {
				ok = false
				break
			}
		}

		if ok {
			cur += 1
		} else {
			c := cur
			idx[c] += 1
			for idx[c] == len(charset) {
				idx[c] = 0
				res[c] = charset[0]
				c -= 1
				idx[c] += 1
			}
			res[c] = charset[idx[c]]
		}
	}
	return res[:]
}

func isUnique(ctx context.Context, encoded []byte, charset []byte) bool {
	revCharset := make([]byte, len(charset))
	for i := 0; i < len(charset); i++ {
		revCharset[len(charset)-i-1] = charset[i]
	}
	s1 := solve(ctx, encoded, charset)
	s2 := solve(ctx, encoded, revCharset)
	if s1 == nil || s2 == nil {
		return false
	}
	return bytes.Equal(s1, s2)
}

func makeMask(batch int, p []int, charset []byte) []byte {
	ctx := context.Background()

	encoded := make([][]byte, batch)
	for i := 0; i < batch; i++ {
		plain := generateChallenge(charset)
		encoded[i] = enc(plain)
	}

	mask := make([]byte, elen)
	count := 0
	for i := 0; i < elen; i++ {
		mask[i] = byte('?')
	}

	for i := 0; i < elen; i++ {
		fmt.Printf(".")

		res := make(chan bool, batch)
		defer close(res)
		ctx2, cancel := context.WithCancel(ctx)
		defer cancel()
		for j := 0; j < batch; j++ {
			go func(j int) {
				tmp := make([]byte, elen)
				copy(tmp, encoded[j])
				tmp[p[i]] = cmask
				r := isUnique(ctx2, tmp, charset)
				res <- r
				if !r {
					cancel()
				}
			}(j)
		}

		ok := true
		for i := 0; i < batch; i++ {
			r := <-res
			if !r {
				ok = false
			}
		}

		if ok {
			mask[p[i]] = cmask
			count++
			for j := 0; j < batch; j++ {
				encoded[j][p[i]] = cmask
			}
		}
	}
	rate := calculateUniqueRate(100, mask, charset)
	fmt.Printf("\n%d / %d, ur = %.02f\nmask: %s\n", elen-count, elen, rate, string(mask))
	return mask
}

func calculateEntropy(itr int, charset []byte) []float64 {
	count := [elen][128]int{}
	for i := 0; i < itr; i++ {
		encoded := enc(generateChallenge(charset))
		for j := 0; j < elen; j++ {
			count[j][encoded[j]]++
		}
	}

	entropy := [elen]float64{}
	for i := 0; i < elen; i++ {
		for j := 0; j < 128; j++ {
			if count[i][j] == 0 {
				continue
			}
			p := float64(count[i][j]) / float64(itr)
			entropy[i] -= p * math.Log(p)
		}
	}
	return entropy[:]
}

func makeRandomMask(batch int, charset []byte) []byte {
	p := rand.Perm(elen)
	return makeMask(batch, p, charset)
}

func makeEntropyMask(batch int, charset []byte) []byte {
	p := make([]int, elen)
	e := calculateEntropy(2048, charset)
	for i := 0; i < elen; i++ {
		p[i] = i
	}
	sort.Slice(p, func(i int, j int) bool {
		return e[p[i]] <= e[p[j]]
	})
	return makeMask(batch, p, charset)
}

func calculateUniqueRate(trial int, mask []byte, charset []byte) float64 {
	count := 0
	ctx := context.Background()
	for i := 0; i < trial; i++ {
		plain := generateChallenge(charset)
		enc := enc(plain)
		for j := 0; j < elen; j++ {
			if mask[j] == cmask {
				enc[j] = cmask
			}
		}
		if isUnique(ctx, enc, charset) {
			count += 1
		}
	}
	return float64(count) / float64(trial)
}

func main() {
	rand.Seed(time.Now().UnixNano())
	makeEntropyMask(64, []byte(defaultCharset))
}

# This is DSA

## Author

@hakatashi, @naan4UGen

## Description

DSA is too hard for me. Could you help me build it?

---

![](https://i.imgur.com/Ew9RAvy.png)

* [dist](dist)

## TSGer向け

* pycryptodomeの private fork である tsg-ut/pycryptodome を使用するため、ローカルで動かすにはGitHubのトークンが必要です。
  * https://github.com/settings/tokens から生成してください。
* Dockerイメージのビルド手順は以下のとおりです。

  ```
  docker-compose build --build-arg GITHUB_TOKEN=<GitHubトークン>
  docker-compose up
  ```

* **一度ビルドしたらトークンはrevokeしてください。**

## Estimated Difficulty

medium-hard

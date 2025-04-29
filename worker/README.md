Tokens:
1. iam token for `yandex-cloud ml sdk`
```bash
curl \                                                                                         
  --request POST \
  --data '{"yandexPassportOauthToken": "<your_yandex_oauth_token>"}' \
  https://iam.api.cloud.yandex.net/iam/v1/tokens
```
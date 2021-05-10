# CryptoSearch

### Requirements

* Python + pip + venv
* Docker

### Validation

`make validate`

### Local development

`docker-compose up`

### Endpoints

```
POST /auth/register/ -> registered user
POST /auth/login/ -> auth token

GET /crypto/(eth|btc|bch)/addresses/<address>/transactions/ -> transactions for address
GET /crypto/(eth|btc|bch)/transactions/<tx>/ -> transaction detail

GET /crypto/searches/addresses/ -> list of address searches
GET /crypto/searches/transactions/ -> list of address searches

GET/POST /my/addresses -> list/create my addresses
DELETE /my/addresses/ -> remove my address (needs crypto query parameter)
GET /my/balances/ -> list of addresses with their balances
 ```

### Missing improvements

1. Addresses lack common format. (e.g. bitcoin cash returns `bitcoincash:<hash>`)
2. Haven't investigated too deep, but I think values & balances also differ between cryptos
3. Blockchain client structure is not great, should have done per API clients, not per-currency.
4. There could be better alternatives for return objects for blockchain client
5. Lack of validations in general

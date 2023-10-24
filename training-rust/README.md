### NSQ
```bash
# Publish message
curl -d "{\'hello\':\'world\'}" http://nsqd-1:4151/pub?topic=training-rust
```
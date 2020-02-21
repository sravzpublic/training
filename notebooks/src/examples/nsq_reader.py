import nsq
import ssl

def handler(message):
    print(message.body)
    return True

r = nsq.Reader(message_handler=handler,
        lookupd_http_addresses=['http://vagrant.sravz.com:4161'],
        topic='test', channel='asdf',
        # tls_v1=True,
        # tls_options={
        #     'cert_reqs': ssl.CERT_NONE,
        #     'ssl_version': ssl.PROTOCOL_TLSv1,
        #     'certfile': '/tmp/cert.pem',
        #     'keyfile': '/tmp/key.key',
        #     # 'ca_certs': '/tmp/nsqtmp/CAroot.pem',
        # },
        lookupd_poll_interval=15)
nsq.run()
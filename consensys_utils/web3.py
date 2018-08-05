"""
    consensys_utils.web3
    ~~~~~~~~~~~~~~~~~~~~

    Implement Web3 resources

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""


def create_provider(config):
    """Create a web3.py provider

    :param config: Provider configuration (compatible with :meth:`consensys_utils.config.schema.web3.Web3ConfigSchema`)
    :type config: dict
    """
    provider, opts = config.get('ETHEREUM_PROVIDER'), config.get('ETHEREUM_OPTS', {})

    if provider == 'http':
        from web3 import HTTPProvider
        return HTTPProvider(endpoint_uri=config.get('ETHEREUM_ENDPOINT_URI'), **opts)

    elif provider == 'ipc':
        from web3 import IPCProvider
        return IPCProvider(ipc_path=config.get('ETHEREUM_IPC_PATH'), **opts)

    elif provider == 'ws':
        from web3 import WebsocketProvider
        return WebsocketProvider(endpoint_uri=config.get('ETHEREUM_ENDPOINT_URI'), **opts)

    elif provider == 'test':
        from web3 import EthereumTesterProvider
        return EthereumTesterProvider()

    else:
        raise RuntimeError("'ETHEREUM_PROVIDER' configuration must be one of 'http', 'ipc', 'ws', 'test'")

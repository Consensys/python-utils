"""
    consensys_utils.config.schema.web3
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Web3 configuration schema

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import cfg_loader

from marshmallow import fields


class Web3ConfigSchema(cfg_loader.ConfigSchema):
    """Logging configuration schema

       Describes and validates against

       .. list-table::
           :widths: 30 50 20
           :header-rows: 1

           * - Key
             - Comment
             - Default value

           * - ``ETHEREUM_PROVIDER``
             - Ethereum provider to use (can be either ``http``, ``ipc``, ``ws`` or ``test``)
             - ``http``

           * - ``ETHEREUM_ENDPOINT_URI``
             - Ethereum node endpoint url
             - ``http://localhost:8545``

           * - ``ETHEREUM_IPC_PATH``
             - Ethereum ipc path
             -

           * - ``ETHEREUM_OPTS``
             - Options to pass when instantiating Ethereum provider
             - ``{}``
       """

    ETHEREUM_PROVIDER = fields.Str(missing='http')
    ETHEREUM_ENDPOINT_URI = fields.Str(missing='http://localhost:8545')
    ETHEREUM_IPC_PATH = fields.Str()
    ETHEREUM_OPTS = fields.Dict()

"""
    consensys_utils.config.schema.gunicorn
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Gunicorn configuration schema

    :copyright: Copyright 2017 by ConsenSys France.
    :license: BSD, see :ref:`license` for more details.
"""

import cfg_loader
from cfg_loader.fields import Path, UnwrapNested
from marshmallow import fields


class DebuggingConfigSchema(cfg_loader.ConfigSchema):
    """Debugging configuration

    c.f http://docs.gunicorn.org/en/stable/settings.html#debugging
    """

    reload = fields.Bool(missing=False)
    reload_engine = fields.Str(missing='auto')
    reload_extra_files = fields.List(Path(), missing=[])
    spew = fields.Bool(missing=False)
    check_config = fields.Bool(missing=False)


class LoggingConfigSchema(cfg_loader.ConfigSchema):
    """Logging configuration

    c.f http://docs.gunicorn.org/en/stable/settings.html#logging
    """

    accesslog = fields.Str()
    disable_redirect_access_to_syslog = fields.Bool(missing=False)
    access_log_format = fields.Str(missing='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"')
    errorlog = fields.Str(missing='-')
    loglevel = fields.Str(missing='info')
    capture_output = fields.Bool(missing=False)
    logger_class = fields.Str(missing='consensys_utils.gunicorn.logging.Logger')
    logconfig = fields.Str()
    logconfig_dict = fields.Dict()
    syslog_addr = fields.Str(missing='udp://localhost:514')
    syslog = fields.Bool(missing=False)
    syslog_prefix = fields.Str()
    syslog_facility = fields.Str(missing='user')
    enable_stdio_inheritance = fields.Bool(missing=False)
    statsd_host = fields.Str()
    statsd_prefix = fields.Str(missing='')


class ProcessNamingConfigSchema(cfg_loader.ConfigSchema):
    """Process Naming configuration

    c.f http://docs.gunicorn.org/en/stable/settings.html#process-naming
    """

    proc_name = fields.Str()
    default_proc_name = fields.Str(missing='gunicorn')


class SSLConfigSchema(cfg_loader.ConfigSchema):
    """SSL configuration

    c.f http://docs.gunicorn.org/en/stable/settings.html#ssl
    """

    keyfile = Path()
    certfile = Path()
    ssl_version = fields.Str(missing='2')
    cert_reqs = fields.Str(missing='0')
    ca_certs = Path()
    suppress_ragged_eofs = fields.Bool(missing=True)
    do_handshake_on_connect = fields.Bool(missing=False)
    ciphers = fields.Str(missing='TLSv1')


class SecurityConfigSchema(cfg_loader.ConfigSchema):
    """Security configuration

    c.f http://docs.gunicorn.org/en/stable/settings.html#security
    """

    limit_request_line = fields.Int(missing=4094)
    limit_request_fields = fields.Int(missing=100)
    limit_request_field_size = fields.Int(missing=8190)


class ServerMechanicsConfigSchema(cfg_loader.ConfigSchema):
    """Server Mechanics configuration

    c.f http://docs.gunicorn.org/en/stable/settings.html#server-mechanics
    """

    preload_app = fields.Bool(missing=False)
    sendfile = fields.Bool()
    reuse_port = fields.Bool(missing=False)
    chdir = fields.Str()
    daemon = fields.Bool(missing=False)
    raw_env = fields.List(fields.Str(), missing=[])
    pidfile = fields.Str()
    worker_tmp_dir = fields.Str()
    user = fields.Int(missing=1005)
    group = fields.Int(missing=205)
    umask = fields.Int(missing=0)
    initgroups = fields.Bool(missing=False)
    tmp_upload_dir = fields.Str()
    secure_scheme_headers = fields.Dict(missing={
        'X-FORWARDED-PROTOCOL': 'ssl',
        'X-FORWARDED-PROTO': 'https',
        'X-FORWARDED-SSL': 'on',
    })
    forwarded_allow_ips = fields.Str(missing="127.0.0.1")
    pythonpath = fields.Str()
    paste = fields.Str()
    proxy_protocol = fields.Bool(missing=False)
    proxy_allow_ips = fields.Str(missing="127.0.0.1")
    raw_paste_global_conf = fields.List(fields.Str(), missing=[])


class ServerSocketConfigSchema(cfg_loader.ConfigSchema):
    """Server Socket configuration

    c.f http://docs.gunicorn.org/en/stable/settings.html#server-socket
    """
    bind = fields.List(fields.Str(), missing=[':5000'])
    backlog = fields.Int(missing=2048)


class WorkerProcessesConfigSchema(cfg_loader.ConfigSchema):
    """Worker Processes configuration

    c.f http://docs.gunicorn.org/en/stable/settings.html#worker-processes
    """
    workers = fields.Int(missing=1)
    worker_class = fields.Str(missing='sync')
    threads = fields.Int(missing=1)
    worker_connections = fields.Int(missing=1000)
    max_requests = fields.Int(missing=0)
    max_requests_jitter = fields.Int(missing=0)
    timeout = fields.Int(missing=30)
    graceful_timeout = fields.Int(missing=30)
    keepalive = fields.Int(missing=2)


class GunicornConfigSchema(cfg_loader.ConfigSchema):
    """Gunicorn configuration

    Please refer to http://docs.gunicorn.org/en/stable/settings.html for exhaustive listing of Gunicorn settings.

    Describes and validates against

    .. list-table::
        :widths: 30 50 20
        :header-rows: 1

        * - Key
          - Comment
          - Default value

        * - ``config``
          - Gunicorn config file path
          -

        * - ``debugging``
          - Debugging config in format :class:`DebuggingConfigSchema`
          - :class:`DebuggingConfigSchema` default

        * - ``logging``
          - Gunicorn logging config in format :class:`LoggingConfigSchema`
          - :class:`LoggingConfigSchema` default

        * - ``process-naming``
          - Process naming config in format :class:`ProcessNamingConfigSchema`
          - :class:`ProcessNamingConfigSchema` default

        * - ``ssl``
          - Debugging config in format :class:`SSLConfigSchema`
          - :class:`SSLConfigSchema` default

        * - ``security``
          - Security config in format :class:`SecurityConfigSchema`
          - :class:`SecurityConfigSchema` default

        * - ``server-mechanics``
          - Server mechanics config in format :class:`ServerMechanicsConfigSchema`
          - :class:`ServerMechanicsConfigSchema` default

        * - ``server-socket``
          - Server Socket config in format :class:`ServerSocketConfigSchema`
          - :class:`ServerSocketConfigSchema` default

        * - ``worker-processes``
          - Worker processes config in format :class:`WorkerProcessesConfigSchema`
          - :class:`WorkerProcessesConfigSchema` default
    """

    # Config file
    config = Path()

    # Debugging
    debugging = UnwrapNested(DebuggingConfigSchema,
                             missing=DebuggingConfigSchema().load({}))

    # Logging
    logging = UnwrapNested(LoggingConfigSchema,
                           missing=LoggingConfigSchema().load({}))

    # Process Naming
    process_naming = UnwrapNested(ProcessNamingConfigSchema,
                                  missing=ProcessNamingConfigSchema().load({}),
                                  key='process-naming')

    # SSL
    ssl = UnwrapNested(SSLConfigSchema,
                       missing=SSLConfigSchema().load({}))

    # Security
    security = UnwrapNested(SecurityConfigSchema,
                            missing=SecurityConfigSchema().load({}))

    # Server Mechanics
    server_mechanics = UnwrapNested(ServerMechanicsConfigSchema,
                                    missing=ServerMechanicsConfigSchema().load({}),
                                    data_key='server-mechanics')

    # Server Socket
    server_socket = UnwrapNested(ServerSocketConfigSchema,
                                 missing=ServerSocketConfigSchema().load({}),
                                 data_key='server-socket')

    # Worker Processes
    worker_processes = UnwrapNested(WorkerProcessesConfigSchema,
                                    missing=WorkerProcessesConfigSchema().load({}),
                                    data_key='worker-processes')

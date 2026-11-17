import logging
import sys
import structlog
from structlog.types import Processor
from collections.abc import Sequence


def configure_logging(
    *,
    log_level: str = "INFO",
    json_logging: bool = True,
    service_name: str = "my-service",
    service_version: str = "1.0.0",
    environment: str = "production",
) -> None:
    """Configure structured logging for the application."""
    level = getattr(logging, log_level.upper(), logging.INFO)

    # Shared processors for both structlog and standard logging
    shared_processors: Sequence[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    # JSON or console rendering
    if json_logging:
        renderer: Processor = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(
            colors=True,
            exception_formatter=structlog.dev.plain_traceback
        )

    # Structlog processor chain
    structlog_processors: Sequence[Processor] = [
        *shared_processors,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    # Standard library processor chain
    stdlib_processors: Sequence[Processor] = [
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        renderer,
    ]

    # Configure structlog
    structlog.configure(
        processors=structlog_processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=stdlib_processors,
    )

    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    root_logger.addHandler(handler)

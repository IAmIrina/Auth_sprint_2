from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter()
        )
    )


def request_hook(span, environ):
    if span and span.is_recording():
        request_id = environ.get('HTTP_X_REQUEST_ID')
        span.set_attribute("http.request_id", request_id)


configure_tracer()
tracer = trace.get_tracer(__name__)

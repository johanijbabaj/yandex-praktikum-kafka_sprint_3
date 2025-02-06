from jinja2 import Template
from app.kafka_consumer import consume_messages

def generate_metrics():
    """
    Function to generate metrics in Prometheus format.
    It will listen to Kafka topic and format the metrics accordingly.
    """
    # Template for Prometheus metrics with correct formatting
    template_str = """
    {% for metric in metrics %}
    # HELP {{ metric.Name }} {{ metric.Description }}
    # TYPE {{ metric.Name }} {{ metric.Type }}
    {{ metric.Name }} {{ metric.Value }}
    {% endfor %}
    """

    # Get data from Kafka (will be an infinite loop in production)
    metrics_data = []
    for message in consume_messages():
        # Process each message and prepare it for Prometheus
        for metric_name, metric_data in message.items():
            metrics_data.append(metric_data)

        # Use Jinja2 to render the Prometheus format
        template = Template(template_str)
        rendered = template.render(metrics=metrics_data)

        # Yield the metrics, strip unwanted leading/trailing whitespace
        yield "\n".join([line.strip() for line in rendered.split("\n") if line.strip()])

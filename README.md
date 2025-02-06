# yandex-praktikum-kafka_sprint_3

# Kafka Project - Sprint 3

## Instructions for Running the Project

To start the project, run the following command:
```sh
docker compose up -d
```
This will initialize all necessary services, including Kafka brokers, PostgreSQL, Kafka Connect, Schema Registry, UI components, and monitoring tools.

## TASK 1: Optimizing JDBC Source Connector for Higher Throughput

The goal of this experiment is to maximize the `Source Record Write Rate` in Kafka by tuning the following parameters:

- `batch.size`
- `linger.ms`
- `compression.type`
- `buffer.memory`

### Performance Table

| Experiment | batch.size | linger.ms | compression.type | buffer.memory | Source Record Write Rate (kops/sec) |
|------------|------------|------------|------------------|---------------|------------------------------------|
| 1          | 100        | 0          | none             | 33554432      | 5.21                              |
| 2          | 901120     | 0          | none             | 33554432      | 163                               |
| 3          | 901120     | 10         | none             | 33554432      | 158                               |
| 4          | 901120     | 10         | snappy           | 33554432      | 147                               |
| 5          | 901120     | 0          | snappy           | 33554432      | 140                               |
| 6 batch.max.rows=1000 | 901120     | 0          | none             | 33554432      | 140                    |

### Experiment Results and Analysis

Performance Analysis of Kafka Producer Experiments
The following experiments were conducted on a local machine using Docker Compose to analyze the impact of different Kafka producer configuration parameters on throughput.

- **Test 1:** Low throughput with default `batch.size` → [Test 1](img/test1.img)  
- **Test 2:** Significant improvement with increased `batch.size` → [Test 2](img/test2.img)  
- **Test 3:** Effect of `linger.ms = 10` on performance → [Test 3](img/test3.img)  
- **Test 4:** Impact of `snappy` compression → [Test 4](img/test4.img)  
- **Test 5:** `snappy` compression with `linger.ms = 0` → [Test 5](img/test5.img)  
- **Test 6:** Performance baseline without compression → [Test 6](img/test6.img)  

Key Findings:
1. Increasing batch.size significantly improves performance

    * Experiment 1 (default batch.size of 100) resulted in a very low throughput of 5.21 kops/sec.
    * Increasing batch.size to 901120 (Experiment 2) caused a drastic increase in throughput to 163 kops/sec.
    * This confirms that larger batch sizes reduce the number of network requests, significantly improving message processing speed.
2. Adding linger.ms has a minimal effect on performance

    * Experiment 3 (linger.ms = 10) resulted in a slight drop in throughput (158 kops/sec) compared to Experiment 2 (163 kops/sec).
    * While linger.ms should theoretically allow better message aggregation, in a local test environment with fast message delivery, its effect is minimal.
3. Compression reduces throughput but optimizes network usage

    * Experiment 4 (compression.type = snappy) reduced throughput to 147 kops/sec, and Experiment 5 (compression.type = snappy, linger.ms = 0) further dropped it to 140 kops/sec.
    * Although compression reduces network bandwidth usage, it introduces CPU overhead, leading to slightly lower write rates.
    * The trade-off depends on the deployment environment:
        * If network bandwidth is a bottleneck, compression is beneficial.
        * If CPU performance is more critical, avoiding compression may be preferable.
4. Experiments 5 and 6 show a stable performance baseline

    * The results of Experiments 5 and 6 (batch.size = 901120, linger.ms = 0, no compression) remain consistent at 140 kops/sec.
    * This suggests that beyond a certain point, increasing batch size and disabling compression does not yield further improvements in a local test environment.

<b>Conclusion & Recommendations:</b>

* Best performance configuration for high throughput:

batch.size = 901120, linger.ms = 0, compression.type = none (Experiment 2: 163 kops/sec)
* Balanced configuration for network efficiency:

batch.size = 901120, linger.ms = 10, compression.type = snappy (Experiment 4: 147 kops/sec)
* Compression is recommended only when reducing network traffic is a priority, as it slightly reduces write speed.

🚀 Final takeaway: Tuning batch.size has the most significant impact on Kafka producer performance. Compression should be used selectively based on network constraints.


## TASK 2: Kafka to Prometheus Data Transfer

### **Overview**
This project transfers metrics from Kafka to Prometheus:

- **Kafka**: Receives JSON metrics from a script.
- **FastAPI**: Processes and serves metrics at `/metrics` for Prometheus.
- **Prometheus**: Collects and visualizes metrics from FastAPI.

### **How to Run**

1. Start with Docker Compose:
   ```bash
   docker-compose up --build
   ```bash
2. Check Prometheus metrics at:
[`prometeus`](http://0.0.0.0:9090/graph?g0.expr=TotalMemory&g0.tab=0&g0.stacked=0&g0.show_exemplars=0&g0.range_input=1h).  


## TASK 3: Debezium PostgresConnector Logs  

As part of the **Debezium PostgresConnector** lesson, we configured and tested the connector. The log output from this process has been saved separately for reference.  

You can find the full log output in the file: [`debezium_logs.txt`](./debezium_logs.txt).  

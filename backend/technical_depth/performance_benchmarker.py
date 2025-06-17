import time
import asyncio
import numpy as np
import psutil
import threading
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
import json
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing as mp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BenchmarkResult:
    """Results from a performance benchmark"""
    benchmark_name: str
    execution_time: float
    memory_usage: float
    cpu_usage: float
    throughput: float
    accuracy: Optional[float]
    metadata: Dict[str, Any]
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class SystemMetrics:
    """System performance metrics"""
    cpu_percent: float
    memory_percent: float
    disk_usage: float
    network_io: Dict[str, int]
    process_count: int
    load_average: List[float]
    timestamp: str

class PerformanceBenchmarker:
    """Advanced performance benchmarking system for ML workloads"""
    
    def __init__(self, cache_results: bool = True):
        self.cache_results = cache_results
        self.benchmark_cache = {}
        self.system_monitor = SystemMonitor()
        self.benchmark_registry = self._initialize_benchmarks()
        
    def _initialize_benchmarks(self) -> Dict[str, callable]:
        """Initialize available benchmarks"""
        return {
            'matrix_multiplication': self._benchmark_matrix_multiplication,
            'sorting_algorithms': self._benchmark_sorting_algorithms,
            'ml_training_simulation': self._benchmark_ml_training,
            'data_processing': self._benchmark_data_processing,
            'memory_allocation': self._benchmark_memory_allocation,
            'concurrent_processing': self._benchmark_concurrent_processing,
            'io_operations': self._benchmark_io_operations,
            'neural_network_inference': self._benchmark_nn_inference
        }
        
    async def run_comprehensive_benchmark(self, 
                                        workload_type: str = "mixed",
                                        duration_minutes: int = 5) -> Dict[str, Any]:
        """Run comprehensive performance benchmark suite"""
        
        logger.info(f"Starting comprehensive benchmark: {workload_type}")
        start_time = datetime.now()
        
        # Start system monitoring
        monitor_task = asyncio.create_task(
            self.system_monitor.start_monitoring(duration_minutes * 60)
        )
        
        # Select benchmarks based on workload type
        selected_benchmarks = self._select_benchmarks(workload_type)
        
        # Run benchmarks
        benchmark_results = {}
        
        for benchmark_name in selected_benchmarks:
            logger.info(f"Running benchmark: {benchmark_name}")
            
            try:
                result = await self._run_single_benchmark(benchmark_name)
                benchmark_results[benchmark_name] = result
                
                # Brief pause between benchmarks
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Benchmark {benchmark_name} failed: {e}")
                benchmark_results[benchmark_name] = self._create_error_result(benchmark_name, str(e))
                
        # Stop monitoring and get results
        system_metrics = await monitor_task
        
        # Compile comprehensive results
        comprehensive_results = {
            'benchmark_suite': workload_type,
            'execution_time': (datetime.now() - start_time).total_seconds(),
            'individual_benchmarks': benchmark_results,
            'system_metrics': system_metrics,
            'performance_summary': self._generate_performance_summary(benchmark_results),
            'recommendations': self._generate_performance_recommendations(benchmark_results, system_metrics),
            'timestamp': datetime.now().isoformat()
        }
        
        # Cache results if enabled
        if self.cache_results:
            self._cache_results(comprehensive_results)
            
        return comprehensive_results
        
    async def _run_single_benchmark(self, benchmark_name: str) -> BenchmarkResult:
        """Run a single benchmark and measure performance"""
        
        if benchmark_name not in self.benchmark_registry:
            raise ValueError(f"Unknown benchmark: {benchmark_name}")
            
        # Pre-benchmark system state
        initial_memory = psutil.virtual_memory().percent
        initial_cpu = psutil.cpu_percent(interval=1)
        
        start_time = time.time()
        
        # Run the benchmark
        benchmark_func = self.benchmark_registry[benchmark_name]
        result_data = await benchmark_func()
        
        end_time = time.time()
        
        # Post-benchmark system state
        final_memory = psutil.virtual_memory().percent
        final_cpu = psutil.cpu_percent(interval=1)
        
        # Calculate metrics
        execution_time = end_time - start_time
        memory_usage = final_memory - initial_memory
        cpu_usage = (initial_cpu + final_cpu) / 2
        
        return BenchmarkResult(
            benchmark_name=benchmark_name,
            execution_time=execution_time,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            throughput=result_data.get('throughput', 0),
            accuracy=result_data.get('accuracy'),
            metadata=result_data.get('metadata', {}),
            timestamp=datetime.now().isoformat()
        )
        
    async def _benchmark_matrix_multiplication(self) -> Dict[str, Any]:
        """Benchmark matrix multiplication operations"""
        
        sizes = [100, 500, 1000, 2000]
        results = []
        
        for size in sizes:
            # Generate random matrices
            A = np.random.rand(size, size).astype(np.float32)
            B = np.random.rand(size, size).astype(np.float32)
            
            # Time the multiplication
            start_time = time.time()
            C = np.dot(A, B)
            end_time = time.time()
            
            execution_time = end_time - start_time
            operations = size ** 3 * 2  # Approximate FLOPS
            throughput = operations / execution_time / 1e9  # GFLOPS
            
            results.append({
                'matrix_size': size,
                'execution_time': execution_time,
                'throughput_gflops': throughput
            })
            
        avg_throughput = np.mean([r['throughput_gflops'] for r in results])
        
        return {
            'throughput': avg_throughput,
            'metadata': {
                'detailed_results': results,
                'peak_throughput': max(r['throughput_gflops'] for r in results),
                'test_description': 'Matrix multiplication benchmark across different sizes'
            }
        }
        
    async def _benchmark_sorting_algorithms(self) -> Dict[str, Any]:
        """Benchmark different sorting algorithms"""
        
        algorithms = {
            'numpy_sort': lambda x: np.sort(x),
            'python_sort': lambda x: sorted(x.tolist()),
            'quicksort': self._quicksort_implementation
        }
        
        data_sizes = [1000, 10000, 100000]
        results = {}
        
        for alg_name, alg_func in algorithms.items():
            alg_results = []
            
            for size in data_sizes:
                # Generate random data
                data = np.random.rand(size)
                
                # Time the sorting
                start_time = time.time()
                try:
                    sorted_data = alg_func(data.copy())
                    end_time = time.time()
                    
                    execution_time = end_time - start_time
                    throughput = size / execution_time  # Elements per second
                    
                    alg_results.append({
                        'data_size': size,
                        'execution_time': execution_time,
                        'throughput': throughput
                    })
                    
                except Exception as e:
                    logger.warning(f"Algorithm {alg_name} failed on size {size}: {e}")
                    
            results[alg_name] = alg_results
            
        # Calculate overall performance
        avg_throughput = np.mean([
            np.mean([r['throughput'] for r in alg_results])
            for alg_results in results.values() if alg_results
        ])
        
        return {
            'throughput': avg_throughput,
            'metadata': {
                'algorithm_results': results,
                'test_description': 'Sorting algorithm performance comparison'
            }
        }
        
    async def _benchmark_ml_training(self) -> Dict[str, Any]:
        """Simulate ML training workload"""
        
        # Simulate different ML scenarios
        scenarios = [
            {'name': 'linear_regression', 'features': 100, 'samples': 10000, 'iterations': 1000},
            {'name': 'neural_network', 'features': 784, 'samples': 5000, 'iterations': 500},
            {'name': 'clustering', 'features': 50, 'samples': 20000, 'iterations': 100}
        ]
        
        results = []
        
        for scenario in scenarios:
            # Generate synthetic data
            X = np.random.rand(scenario['samples'], scenario['features'])
            y = np.random.rand(scenario['samples'])
            
            start_time = time.time()
            
            # Simulate training iterations
            for i in range(scenario['iterations']):
                # Simulate gradient computation
                gradients = np.random.rand(scenario['features'])
                
                # Simulate parameter update
                weights = np.random.rand(scenario['features'])
                weights -= 0.01 * gradients
                
                # Simulate loss computation
                predictions = np.dot(X, weights)
                loss = np.mean((predictions - y) ** 2)
                
            end_time = time.time()
            
            execution_time = end_time - start_time
            throughput = scenario['iterations'] / execution_time  # Iterations per second
            
            # Simulate accuracy (would be real in actual ML)
            accuracy = 0.85 + np.random.normal(0, 0.05)
            accuracy = max(0, min(1, accuracy))
            
            results.append({
                'scenario': scenario['name'],
                'execution_time': execution_time,
                'throughput': throughput,
                'accuracy': accuracy,
                'parameters': scenario
            })
            
        avg_throughput = np.mean([r['throughput'] for r in results])
        avg_accuracy = np.mean([r['accuracy'] for r in results])
        
        return {
            'throughput': avg_throughput,
            'accuracy': avg_accuracy,
            'metadata': {
                'scenario_results': results,
                'test_description': 'ML training simulation across different scenarios'
            }
        }
        
    async def _benchmark_data_processing(self) -> Dict[str, Any]:
        """Benchmark data processing operations"""
        
        # Generate large dataset
        data_size = 1000000
        data = {
            'values': np.random.rand(data_size),
            'categories': np.random.choice(['A', 'B', 'C', 'D'], data_size),
            'timestamps': [datetime.now() - timedelta(seconds=i) for i in range(data_size)]
        }
        
        operations = [
            ('filtering', lambda: data['values'][data['values'] > 0.5]),
            ('aggregation', lambda: np.mean(data['values'])),
            ('grouping', lambda: {cat: np.mean(data['values'][np.array(data['categories']) == cat]) 
                                for cat in ['A', 'B', 'C', 'D']}),
            ('sorting', lambda: np.sort(data['values']))
        ]
        
        results = []
        
        for op_name, op_func in operations:
            start_time = time.time()
            result = op_func()
            end_time = time.time()
            
            execution_time = end_time - start_time
            throughput = data_size / execution_time  # Records per second
            
            results.append({
                'operation': op_name,
                'execution_time': execution_time,
                'throughput': throughput
            })
            
        avg_throughput = np.mean([r['throughput'] for r in results])
        
        return {
            'throughput': avg_throughput,
            'metadata': {
                'operation_results': results,
                'data_size': data_size,
                'test_description': 'Data processing operations benchmark'
            }
        }
        
    async def _benchmark_memory_allocation(self) -> Dict[str, Any]:
        """Benchmark memory allocation and deallocation"""
        
        allocation_sizes = [1024, 10240, 102400, 1024000]  # Bytes
        results = []
        
        for size in allocation_sizes:
            # Measure allocation time
            start_time = time.time()
            allocated_arrays = []
            
            for _ in range(100):  # Allocate 100 arrays
                arr = np.zeros(size // 8)  # 8 bytes per float64
                allocated_arrays.append(arr)
                
            allocation_time = time.time() - start_time
            
            # Measure deallocation time
            start_time = time.time()
            del allocated_arrays
            deallocation_time = time.time() - start_time
            
            total_time = allocation_time + deallocation_time
            throughput = (size * 100) / total_time  # Bytes per second
            
            results.append({
                'allocation_size': size,
                'allocation_time': allocation_time,
                'deallocation_time': deallocation_time,
                'total_time': total_time,
                'throughput': throughput
            })
            
        avg_throughput = np.mean([r['throughput'] for r in results])
        
        return {
            'throughput': avg_throughput,
            'metadata': {
                'allocation_results': results,
                'test_description': 'Memory allocation and deallocation benchmark'
            }
        }
        
    async def _benchmark_concurrent_processing(self) -> Dict[str, Any]:
        """Benchmark concurrent processing capabilities"""
        
        def cpu_intensive_task(n):
            """CPU-intensive task for benchmarking"""
            result = 0
            for i in range(n):
                result += i ** 2
            return result
            
        task_size = 100000
        thread_counts = [1, 2, 4, 8, mp.cpu_count()]
        results = []
        
        for thread_count in thread_counts:
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                futures = [executor.submit(cpu_intensive_task, task_size) for _ in range(thread_count)]
                results_list = [future.result() for future in futures]
                
            end_time = time.time()
            
            execution_time = end_time - start_time
            throughput = (task_size * thread_count) / execution_time
            
            results.append({
                'thread_count': thread_count,
                'execution_time': execution_time,
                'throughput': throughput,
                'speedup': results[0]['execution_time'] / execution_time if results else 1.0
            })
            
        max_throughput = max(r['throughput'] for r in results)
        
        return {
            'throughput': max_throughput,
            'metadata': {
                'concurrency_results': results,
                'optimal_thread_count': max(results, key=lambda x: x['throughput'])['thread_count'],
                'test_description': 'Concurrent processing scalability benchmark'
            }
        }
        
    async def _benchmark_io_operations(self) -> Dict[str, Any]:
        """Benchmark I/O operations"""
        
        import tempfile
        import os
        
        file_sizes = [1024, 10240, 102400, 1024000]  # Bytes
        results = []
        
        for size in file_sizes:
            # Generate test data
            test_data = os.urandom(size)
            
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_filename = temp_file.name
                
                # Measure write performance
                start_time = time.time()
                temp_file.write(test_data)
                temp_file.flush()
                os.fsync(temp_file.fileno())
                write_time = time.time() - start_time
                
            # Measure read performance
            start_time = time.time()
            with open(temp_filename, 'rb') as f:
                read_data = f.read()
            read_time = time.time() - start_time
            
            # Clean up
            os.unlink(temp_filename)
            
            write_throughput = size / write_time  # Bytes per second
            read_throughput = size / read_time
            
            results.append({
                'file_size': size,
                'write_time': write_time,
                'read_time': read_time,
                'write_throughput': write_throughput,
                'read_throughput': read_throughput
            })
            
        avg_write_throughput = np.mean([r['write_throughput'] for r in results])
        avg_read_throughput = np.mean([r['read_throughput'] for r in results])
        
        return {
            'throughput': (avg_write_throughput + avg_read_throughput) / 2,
            'metadata': {
                'io_results': results,
                'avg_write_throughput': avg_write_throughput,
                'avg_read_throughput': avg_read_throughput,
                'test_description': 'File I/O operations benchmark'
            }
        }
        
    async def _benchmark_nn_inference(self) -> Dict[str, Any]:
        """Simulate neural network inference benchmark"""
        
        # Simulate different network architectures
        architectures = [
            {'name': 'small_cnn', 'layers': [32, 64, 128], 'input_size': 224},
            {'name': 'medium_mlp', 'layers': [512, 256, 128, 64], 'input_size': 784},
            {'name': 'large_transformer', 'layers': [1024, 1024, 1024], 'input_size': 512}
        ]
        
        results = []
        batch_size = 32
        
        for arch in architectures:
            # Simulate network weights
            weights = []
            prev_size = arch['input_size']
            
            for layer_size in arch['layers']:
                weight_matrix = np.random.rand(prev_size, layer_size).astype(np.float32)
                weights.append(weight_matrix)
                prev_size = layer_size
                
            # Generate batch of inputs
            inputs = np.random.rand(batch_size, arch['input_size']).astype(np.float32)
            
            # Measure inference time
            start_time = time.time()
            
            # Forward pass simulation
            activations = inputs
            for weight_matrix in weights:
                activations = np.dot(activations, weight_matrix)
                activations = np.maximum(0, activations)  # ReLU activation
                
            end_time = time.time()
            
            execution_time = end_time - start_time
            throughput = batch_size / execution_time  # Inferences per second
            
            # Simulate accuracy
            accuracy = 0.90 + np.random.normal(0, 0.03)
            accuracy = max(0, min(1, accuracy))
            
            results.append({
                'architecture': arch['name'],
                'execution_time': execution_time,
                'throughput': throughput,
                'accuracy': accuracy,
                'parameters': arch
            })
            
        avg_throughput = np.mean([r['throughput'] for r in results])
        avg_accuracy = np.mean([r['accuracy'] for r in results])
        
        return {
            'throughput': avg_throughput,
            'accuracy': avg_accuracy,
            'metadata': {
                'architecture_results': results,
                'batch_size': batch_size,
                'test_description': 'Neural network inference simulation'
            }
        }
        
    def _quicksort_implementation(self, arr):
        """Simple quicksort implementation for benchmarking"""
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return self._quicksort_implementation(left) + middle + self._quicksort_implementation(right)
        
    def _select_benchmarks(self, workload_type: str) -> List[str]:
        """Select benchmarks based on workload type"""
        
        benchmark_sets = {
            'mixed': list(self.benchmark_registry.keys()),
            'compute_intensive': [
                'matrix_multiplication', 'ml_training_simulation', 
                'neural_network_inference', 'concurrent_processing'
            ],
            'memory_intensive': [
                'memory_allocation', 'data_processing', 'sorting_algorithms'
            ],
            'io_intensive': [
                'io_operations', 'data_processing'
            ],
            'ml_focused': [
                'ml_training_simulation', 'neural_network_inference', 
                'matrix_multiplication', 'data_processing'
            ]
        }
        
        return benchmark_sets.get(workload_type, benchmark_sets['mixed'])
        
    def _generate_performance_summary(self, benchmark_results: Dict[str, BenchmarkResult]) -> Dict[str, Any]:
        """Generate performance summary from benchmark results"""
        
        if not benchmark_results:
            return {}
            
        # Calculate aggregate metrics
        total_execution_time = sum(r.execution_time for r in benchmark_results.values())
        avg_cpu_usage = np.mean([r.cpu_usage for r in benchmark_results.values()])
        avg_memory_usage = np.mean([r.memory_usage for r in benchmark_results.values()])
        avg_throughput = np.mean([r.throughput for r in benchmark_results.values() if r.throughput > 0])
        
        # Find best and worst performing benchmarks
        best_benchmark = max(benchmark_results.items(), key=lambda x: x[1].throughput)
        worst_benchmark = min(benchmark_results.items(), key=lambda x: x[1].throughput)
        
        return {
            'total_execution_time': total_execution_time,
            'average_cpu_usage': avg_cpu_usage,
            'average_memory_usage': avg_memory_usage,
            'average_throughput': avg_throughput,
            'best_performing_benchmark': {
                'name': best_benchmark[0],
                'throughput': best_benchmark[1].throughput
            },
            'worst_performing_benchmark': {
                'name': worst_benchmark[0],
                'throughput': worst_benchmark[1].throughput
            },
            'benchmark_count': len(benchmark_results),
            'success_rate': len([r for r in benchmark_results.values() if r.throughput > 0]) / len(benchmark_results)
        }
        
    def _generate_performance_recommendations(self, 
                                           benchmark_results: Dict[str, BenchmarkResult],
                                           system_metrics: List[SystemMetrics]) -> List[str]:
        """Generate performance recommendations based on results"""
        
        recommendations = []
        
        if not benchmark_results or not system_metrics:
            return ["Insufficient data for recommendations"]
            
        # Analyze CPU usage
        avg_cpu = np.mean([m.cpu_percent for m in system_metrics])
        if avg_cpu > 80:
            recommendations.append("High CPU usage detected - consider CPU optimization or scaling")
        elif avg_cpu < 30:
            recommendations.append("Low CPU utilization - workload may be I/O or memory bound")
            
        # Analyze memory usage
        avg_memory = np.mean([m.memory_percent for m in system_metrics])
        if avg_memory > 85:
            recommendations.append("High memory usage - consider memory optimization or more RAM")
        elif avg_memory < 40:
            recommendations.append("Low memory utilization - system has capacity for larger workloads")
            
        # Analyze benchmark performance
        throughputs = [r.throughput for r in benchmark_results.values() if r.throughput > 0]
        if throughputs:
            throughput_variance = np.var(throughputs)
            if throughput_variance > np.mean(throughputs):
                recommendations.append("High performance variance - some workloads may need optimization")
                
        # Specific benchmark recommendations
        if 'concurrent_processing' in benchmark_results:
            concurrent_result = benchmark_results['concurrent_processing']
            optimal_threads = concurrent_result.metadata.get('optimal_thread_count', 1)
            if optimal_threads < mp.cpu_count():
                recommendations.append(f"Concurrency bottleneck detected - optimal thread count is {optimal_threads}")
                
        if 'io_operations' in benchmark_results:
            io_result = benchmark_results['io_operations']
            if io_result.throughput < 1000000:  # Less than 1MB/s
                recommendations.append("I/O performance is low - consider SSD upgrade or I/O optimization")
                
        return recommendations or ["System performance appears optimal for current workloads"]
        
    def _create_error_result(self, benchmark_name: str, error_message: str) -> BenchmarkResult:
        """Create error result for failed benchmarks"""
        return BenchmarkResult(
            benchmark_name=benchmark_name,
            execution_time=0.0,
            memory_usage=0.0,
            cpu_usage=0.0,
            throughput=0.0,
            accuracy=None,
            metadata={'error': error_message},
            timestamp=datetime.now().isoformat()
        )
        
    def _cache_results(self, results: Dict[str, Any]):
        """Cache benchmark results"""
        cache_key = f"{results['benchmark_suite']}_{datetime.now().strftime('%Y%m%d_%H')}"
        self.benchmark_cache[cache_key] = results
        
        # Limit cache size
        if len(self.benchmark_cache) > 100:
            oldest_key = min(self.benchmark_cache.keys())
            del self.benchmark_cache[oldest_key]

class SystemMonitor:
    """System performance monitoring"""
    
    def __init__(self):
        self.monitoring = False
        self.metrics_history = []
        
    async def start_monitoring(self, duration_seconds: int) -> List[SystemMetrics]:
        """Start system monitoring for specified duration"""
        
        self.monitoring = True
        self.metrics_history = []
        
        start_time = time.time()
        
        while self.monitoring and (time.time() - start_time) < duration_seconds:
            metrics = self._collect_system_metrics()
            self.metrics_history.append(metrics)
            
            await asyncio.sleep(1)  # Collect metrics every second
            
        self.monitoring = False
        return self.metrics_history
        
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.monitoring = False
        
    def _collect_system_metrics(self) -> SystemMetrics:
        """Collect current system metrics"""
        
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=None)
        
        # Memory metrics
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Disk metrics
        disk = psutil.disk_usage('/')
        disk_usage = (disk.used / disk.total) * 100
        
        # Network metrics
        network = psutil.net_io_counters()
        network_io = {
            'bytes_sent': network.bytes_sent,
            'bytes_recv': network.bytes_recv
        }
        
        # Process count
        process_count = len(psutil.pids())
        
        # Load average (Unix-like systems)
        try:
            load_average = list(os.getloadavg())
        except (AttributeError, OSError):
            load_average = [0.0, 0.0, 0.0]  # Windows fallback
            
        return SystemMetrics(
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            disk_usage=disk_usage,
            network_io=network_io,
            process_count=process_count,
            load_average=load_average,
            timestamp=datetime.now().isoformat()
        )

# Example usage and testing
async def main():
    """Example usage of the performance benchmarker"""
    
    benchmarker = PerformanceBenchmarker()
    
    # Run comprehensive benchmark
    results = await benchmarker.run_comprehensive_benchmark(
        workload_type="ml_focused",
        duration_minutes=2
    )
    
    # Print results
    print(json.dumps(results, indent=2, default=str))

if __name__ == "__main__":
    asyncio.run(main()) 
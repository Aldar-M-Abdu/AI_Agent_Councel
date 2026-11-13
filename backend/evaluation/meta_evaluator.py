import json
import re
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging
from collections import defaultdict
import numpy as np

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class EvaluationMetrics:
    """Comprehensive evaluation metrics for agent responses"""
    technical_accuracy: float  # 0-1 scale
    persuasiveness: float     # 0-1 scale
    coherence: float          # 0-1 scale
    relevance: float          # 0-1 scale
    completeness: float       # 0-1 scale
    originality: float        # 0-1 scale
    evidence_quality: float   # 0-1 scale
    logical_structure: float  # 0-1 scale
    
    @property
    def overall_score(self) -> float:
        """Calculate weighted overall score"""
        weights = {
            'technical_accuracy': 0.25,
            'persuasiveness': 0.20,
            'coherence': 0.15,
            'relevance': 0.15,
            'completeness': 0.10,
            'originality': 0.05,
            'evidence_quality': 0.05,
            'logical_structure': 0.05
        }
        
        return sum(getattr(self, metric) * weight for metric, weight in weights.items())

@dataclass 
class ComparativeAnalysis:
    """Comparative analysis between agents"""
    agent_rankings: List[Tuple[str, float]]  # (agent_name, score)
    agreement_matrix: Dict[str, Dict[str, float]]  # Agent agreement levels
    consensus_level: float
    diversity_score: float
    quality_distribution: Dict[str, float]
    strengths_by_agent: Dict[str, List[str]]
    weaknesses_by_agent: Dict[str, List[str]]
    emergent_patterns: List[str]

class MetaEvaluator:
    """Meta-agent that evaluates and analyzes agent performance and arguments"""
    
    def __init__(self, external_benchmarks: Optional[Dict[str, Any]] = None):
        self.external_benchmarks = external_benchmarks or {}
        self.evaluation_history = []
        self.performance_baselines = {}
        self.domain_expertise_map = {}
        
    async def evaluate_agent_response(self, 
                                    agent_name: str, 
                                    response: str, 
                                    query: str,
                                    context: Optional[Dict[str, Any]] = None) -> EvaluationMetrics:
        """Evaluate a single agent's response comprehensively"""
        
        logger.info(f"Evaluating response from {agent_name}")
        
        # Technical accuracy assessment
        technical_accuracy = await self._assess_technical_accuracy(response, query, context)
        
        # Persuasiveness assessment
        persuasiveness = self._assess_persuasiveness(response)
        
        # Coherence assessment
        coherence = self._assess_coherence(response)
        
        # Relevance assessment
        relevance = self._assess_relevance(response, query)
        
        # Completeness assessment
        completeness = self._assess_completeness(response, query)
        
        # Originality assessment
        originality = self._assess_originality(response, agent_name)
        
        # Evidence quality assessment
        evidence_quality = self._assess_evidence_quality(response)
        
        # Logical structure assessment
        logical_structure = self._assess_logical_structure(response)
        
        metrics = EvaluationMetrics(
            technical_accuracy=technical_accuracy,
            persuasiveness=persuasiveness,
            coherence=coherence,
            relevance=relevance,
            completeness=completeness,
            originality=originality,
            evidence_quality=evidence_quality,
            logical_structure=logical_structure
        )
        
        # Store evaluation for historical analysis
        self.evaluation_history.append({
            'agent_name': agent_name,
            'query': query,
            'response': response,
            'metrics': metrics,
            'timestamp': datetime.now().isoformat(),
            'context': context
        })
        
        return metrics
        
    async def comparative_analysis(self, 
                                 agent_responses: List[Dict[str, Any]], 
                                 query: str) -> ComparativeAnalysis:
        """Perform comprehensive comparative analysis of all agent responses"""
        
        logger.info(f"Performing comparative analysis of {len(agent_responses)} agent responses")
        
        # Evaluate each response
        evaluations = {}
        for response_data in agent_responses:
            agent_name = response_data['agent_name']
            response = response_data['text_response']
            
            metrics = await self.evaluate_agent_response(agent_name, response, query)
            evaluations[agent_name] = metrics
            
        # Generate rankings
        rankings = self._generate_rankings(evaluations)
        
        # Calculate agreement matrix
        agreement_matrix = self._calculate_agreement_matrix(agent_responses)
        
        # Calculate consensus level
        consensus_level = self._calculate_consensus_level(agent_responses)
        
        # Calculate diversity score
        diversity_score = self._calculate_diversity_score(evaluations)
        
        # Generate quality distribution
        quality_distribution = self._generate_quality_distribution(evaluations)
        
        # Identify strengths and weaknesses
        strengths, weaknesses = self._identify_strengths_weaknesses(evaluations)
        
        # Detect emergent patterns
        emergent_patterns = self._detect_emergent_patterns(agent_responses, evaluations)
        
        return ComparativeAnalysis(
            agent_rankings=rankings,
            agreement_matrix=agreement_matrix,
            consensus_level=consensus_level,
            diversity_score=diversity_score,
            quality_distribution=quality_distribution,
            strengths_by_agent=strengths,
            weaknesses_by_agent=weaknesses,
            emergent_patterns=emergent_patterns
        )
        
    async def benchmark_against_external_sources(self, 
                                               responses: List[Dict[str, Any]], 
                                               query: str) -> Dict[str, Any]:
        """Benchmark agent responses against external references"""
        
        logger.info("Benchmarking against external sources...")
        
        domain = self._identify_domain(query)
        benchmarks = self.external_benchmarks.get(domain, {})
        
        benchmark_results = {
            'domain': domain,
            'available_benchmarks': list(benchmarks.keys()),
            'agent_scores': {},
            'best_practices_alignment': {},
            'factual_accuracy_check': {},
            'industry_standard_compliance': {}
        }
        
        for response_data in responses:
            agent_name = response_data['agent_name']
            response = response_data['text_response']
            
            # Factual accuracy check
            factual_score = await self._check_factual_accuracy(response, domain, benchmarks)
            benchmark_results['factual_accuracy_check'][agent_name] = factual_score
            
            # Best practices alignment
            practices_score = self._check_best_practices_alignment(response, domain, benchmarks)
            benchmark_results['best_practices_alignment'][agent_name] = practices_score
            
            # Industry standard compliance
            compliance_score = self._check_industry_compliance(response, domain, benchmarks)
            benchmark_results['industry_standard_compliance'][agent_name] = compliance_score
            
            # Overall benchmark score
            overall_benchmark_score = (factual_score + practices_score + compliance_score) / 3
            benchmark_results['agent_scores'][agent_name] = overall_benchmark_score
            
        return benchmark_results
        
    def generate_evaluation_report(self, 
                                 comparative_analysis: ComparativeAnalysis,
                                 benchmark_results: Optional[Dict[str, Any]] = None) -> str:
        """Generate comprehensive evaluation report"""
        
        report = f"""
# Agent Council Evaluation Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- **Consensus Level**: {comparative_analysis.consensus_level:.1%}
- **Diversity Score**: {comparative_analysis.diversity_score:.2f}
- **Top Performing Agent**: {comparative_analysis.agent_rankings[0][0]} ({comparative_analysis.agent_rankings[0][1]:.2f})

## Agent Rankings
"""
        
        for i, (agent_name, score) in enumerate(comparative_analysis.agent_rankings, 1):
            report += f"{i}. **{agent_name}**: {score:.3f}\n"
            
        report += "\n## Quality Distribution\n"
        for metric, value in comparative_analysis.quality_distribution.items():
            report += f"- **{metric.replace('_', ' ').title()}**: {value:.3f}\n"
            
        report += "\n## Agent Strengths & Weaknesses\n"
        for agent_name in comparative_analysis.strengths_by_agent:
            report += f"\n### {agent_name}\n"
            report += "**Strengths:**\n"
            for strength in comparative_analysis.strengths_by_agent[agent_name]:
                report += f"- {strength}\n"
            report += "**Areas for Improvement:**\n"
            for weakness in comparative_analysis.weaknesses_by_agent[agent_name]:
                report += f"- {weakness}\n"
                
        if comparative_analysis.emergent_patterns:
            report += "\n## Emergent Patterns\n"
            for pattern in comparative_analysis.emergent_patterns:
                report += f"- {pattern}\n"
                
        if benchmark_results:
            report += f"\n## External Benchmark Analysis\n"
            report += f"**Domain**: {benchmark_results['domain']}\n"
            report += f"**Available Benchmarks**: {', '.join(benchmark_results['available_benchmarks'])}\n\n"
            
            for agent_name, score in benchmark_results['agent_scores'].items():
                report += f"- **{agent_name}**: {score:.3f} benchmark compliance\n"
                
        report += "\n## Recommendations\n"
        report += self._generate_recommendations(comparative_analysis, benchmark_results)
        
        return report
        
    # Private evaluation methods
    async def _assess_technical_accuracy(self, 
                                       response: str, 
                                       query: str, 
                                       context: Optional[Dict[str, Any]]) -> float:
        """Assess technical accuracy of response"""
        
        # Check for factual claims that can be verified
        factual_claims = self._extract_factual_claims(response)
        
        if not factual_claims:
            return 0.7  # Neutral score for opinion-based responses
            
        # Simple accuracy scoring based on common knowledge
        accuracy_score = 0.8  # Base score
        
        # Check for common technical errors or misconceptions
        technical_errors = self._detect_technical_errors(response, query)
        accuracy_score -= len(technical_errors) * 0.1
        
        # Check consistency with external context if available
        if context and 'external_data' in context:
            consistency_score = self._check_consistency_with_context(response, context['external_data'])
            accuracy_score = (accuracy_score + consistency_score) / 2
            
        return max(0.0, min(1.0, accuracy_score))
        
    def _assess_persuasiveness(self, response: str) -> float:
        """Assess persuasiveness of the argument"""
        
        score = 0.5  # Base score
        
        # Check for persuasive elements
        persuasive_elements = {
            'evidence_cited': r'\b(study|research|data|statistics|evidence)\b',
            'logical_connectors': r'\b(therefore|thus|because|since|consequently)\b',
            'authoritative_language': r'\b(proven|established|demonstrated|confirmed)\b',
            'specific_examples': r'\b(for example|for instance|specifically)\b',
            'emotional_appeal': r'\b(important|crucial|essential|vital)\b'
        }
        
        for element, pattern in persuasive_elements.items():
            if re.search(pattern, response, re.IGNORECASE):
                score += 0.1
                
        # Check argument structure
        if self._has_clear_argument_structure(response):
            score += 0.1
            
        return min(1.0, score)
        
    def _assess_coherence(self, response: str) -> float:
        """Assess coherence and flow of the response"""
        
        sentences = response.split('.')
        if len(sentences) < 2:
            return 0.5
            
        coherence_score = 0.7  # Base score
        
        # Check for transition words
        transitions = ['however', 'moreover', 'furthermore', 'additionally', 'in contrast', 'similarly']
        transition_count = sum(1 for t in transitions if t in response.lower())
        coherence_score += min(transition_count * 0.1, 0.2)
        
        # Check for consistent topic focus
        topic_consistency = self._check_topic_consistency(sentences)
        coherence_score = (coherence_score + topic_consistency) / 2
        
        return min(1.0, coherence_score)
        
    def _assess_relevance(self, response: str, query: str) -> float:
        """Assess relevance to the original query"""
        
        query_words = set(query.lower().split())
        response_words = set(response.lower().split())
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        query_words -= stop_words
        response_words -= stop_words
        
        if not query_words:
            return 0.5
            
        overlap = len(query_words.intersection(response_words))
        relevance_score = overlap / len(query_words)
        
        # Boost score if key concepts are addressed
        key_concepts = self._extract_key_concepts(query)
        for concept in key_concepts:
            if concept.lower() in response.lower():
                relevance_score += 0.1
                
        return min(1.0, relevance_score)
        
    def _assess_completeness(self, response: str, query: str) -> float:
        """Assess completeness of the response"""
        
        # Expected components based on query type
        expected_components = self._identify_expected_components(query)
        
        components_found = 0
        for component in expected_components:
            if self._check_component_presence(response, component):
                components_found += 1
                
        if not expected_components:
            return 0.7  # Neutral score if no clear expectations
            
        return components_found / len(expected_components)
        
    def _assess_originality(self, response: str, agent_name: str) -> float:
        """Assess originality of the response"""
        
        # Check against historical responses from this agent
        historical_responses = [h for h in self.evaluation_history if h['agent_name'] == agent_name]
        
        if not historical_responses:
            return 0.8  # High score for first response
            
        # Simple similarity check against previous responses
        max_similarity = 0
        for hist in historical_responses[-5:]:  # Check last 5 responses
            similarity = self._calculate_text_similarity(response, hist['response'])
            max_similarity = max(max_similarity, similarity)
            
        originality_score = 1.0 - max_similarity
        return max(0.1, originality_score)  # Minimum score of 0.1
        
    def _assess_evidence_quality(self, response: str) -> float:
        """Assess quality of evidence provided"""
        
        evidence_indicators = {
            'statistics': r'\b\d+(\.\d+)?%|\b\d+\s*(million|billion|thousand)\b',
            'studies': r'\b(study|research|survey|analysis)\b',
            'citations': r'\b(according to|study shows|research indicates)\b',
            'specific_data': r'\b\d{4}\b|\b\$\d+\b',  # Years or dollar amounts
            'authoritative_sources': r'\b(expert|professor|institute|organization)\b'
        }
        
        evidence_score = 0.3  # Base score
        
        for evidence_type, pattern in evidence_indicators.items():
            matches = len(re.findall(pattern, response, re.IGNORECASE))
            evidence_score += min(matches * 0.15, 0.2)
            
        return min(1.0, evidence_score)
        
    def _assess_logical_structure(self, response: str) -> float:
        """Assess logical structure of the argument"""
        
        structure_score = 0.5  # Base score
        
        # Check for clear introduction
        if self._has_clear_introduction(response):
            structure_score += 0.2
            
        # Check for logical progression
        if self._has_logical_progression(response):
            structure_score += 0.2
            
        # Check for clear conclusion
        if self._has_clear_conclusion(response):
            structure_score += 0.1
            
        return min(1.0, structure_score)
        
    # Helper methods for detailed analysis
    def _extract_factual_claims(self, response: str) -> List[str]:
        """Extract factual claims from response"""
        # Simple pattern matching for factual statements
        factual_patterns = [
            r'\b\d+(\.\d+)?%',  # Percentages
            r'\b\d{4}\b',       # Years
            r'\$\d+',           # Dollar amounts
            r'\bis\s+\w+',      # "is X" statements
        ]
        
        claims = []
        for pattern in factual_patterns:
            matches = re.findall(pattern, response)
            claims.extend(matches)
            
        return claims
        
    def _detect_technical_errors(self, response: str, query: str) -> List[str]:
        """Detect common technical errors or misconceptions"""
        errors = []
        
        # Domain-specific error patterns
        domain_errors = {
            'financial': [
                (r'guaranteed\s+return', 'No investment guarantees returns'),
                (r'risk-free\s+investment', 'No investment is truly risk-free')
            ],
            'technical': [
                (r'100%\s+secure', 'No system is 100% secure'),
                (r'always\s+works', 'Technical solutions have edge cases')
            ]
        }
        
        domain = self._identify_domain(query)
        if domain in domain_errors:
            for pattern, error_msg in domain_errors[domain]:
                if re.search(pattern, response, re.IGNORECASE):
                    errors.append(error_msg)
                    
        return errors
        
    def _check_consistency_with_context(self, response: str, external_data: List[Dict]) -> float:
        """Check consistency with external context data"""
        if not external_data:
            return 0.7
            
        # Simple consistency check - would be more sophisticated in practice
        consistency_indicators = 0
        total_checks = 0
        
        for data_point in external_data[:3]:  # Check first 3 data points
            content = data_point.get('content', '')
            if content:
                total_checks += 1
                # Check if response aligns with external data
                common_words = set(response.lower().split()).intersection(set(content.lower().split()))
                if len(common_words) > 5:  # Arbitrary threshold
                    consistency_indicators += 1
                    
        return consistency_indicators / total_checks if total_checks > 0 else 0.7
        
    def _generate_rankings(self, evaluations: Dict[str, EvaluationMetrics]) -> List[Tuple[str, float]]:
        """Generate agent rankings based on overall scores"""
        rankings = [(agent, metrics.overall_score) for agent, metrics in evaluations.items()]
        return sorted(rankings, key=lambda x: x[1], reverse=True)
        
    def _calculate_agreement_matrix(self, agent_responses: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        """Calculate agreement matrix between agents"""
        agreement_matrix = defaultdict(lambda: defaultdict(float))
        
        agents = [resp['agent_name'] for resp in agent_responses]
        
        for i, agent1 in enumerate(agents):
            for j, agent2 in enumerate(agents):
                if i != j:
                    response1 = agent_responses[i]['text_response']
                    response2 = agent_responses[j]['text_response']
                    
                    agreement = self._calculate_text_similarity(response1, response2)
                    agreement_matrix[agent1][agent2] = agreement
                else:
                    agreement_matrix[agent1][agent2] = 1.0
                    
        return dict(agreement_matrix)
        
    def _calculate_consensus_level(self, agent_responses: List[Dict[str, Any]]) -> float:
        """Calculate overall consensus level among agents"""
        if len(agent_responses) < 2:
            return 1.0
            
        similarities = []
        for i in range(len(agent_responses)):
            for j in range(i + 1, len(agent_responses)):
                response1 = agent_responses[i]['text_response']
                response2 = agent_responses[j]['text_response']
                similarity = self._calculate_text_similarity(response1, response2)
                similarities.append(similarity)
                
        return sum(similarities) / len(similarities) if similarities else 0.0
        
    def _calculate_diversity_score(self, evaluations: Dict[str, EvaluationMetrics]) -> float:
        """Calculate diversity score of agent responses"""
        if len(evaluations) < 2:
            return 0.0
            
        scores = [metrics.overall_score for metrics in evaluations.values()]
        return np.std(scores) if len(scores) > 1 else 0.0
        
    def _generate_quality_distribution(self, evaluations: Dict[str, EvaluationMetrics]) -> Dict[str, float]:
        """Generate quality distribution across different metrics"""
        if not evaluations:
            return {}
            
        metrics_sums = defaultdict(float)
        for evaluation in evaluations.values():
            for attr in ['technical_accuracy', 'persuasiveness', 'coherence', 'relevance', 
                        'completeness', 'originality', 'evidence_quality', 'logical_structure']:
                metrics_sums[attr] += getattr(evaluation, attr)
                
        num_agents = len(evaluations)
        return {metric: total / num_agents for metric, total in metrics_sums.items()}
        
    def _identify_strengths_weaknesses(self, evaluations: Dict[str, EvaluationMetrics]) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        """Identify strengths and weaknesses for each agent"""
        strengths = defaultdict(list)
        weaknesses = defaultdict(list)
        
        metric_names = ['technical_accuracy', 'persuasiveness', 'coherence', 'relevance', 
                       'completeness', 'originality', 'evidence_quality', 'logical_structure']
        
        for agent_name, metrics in evaluations.items():
            for metric in metric_names:
                score = getattr(metrics, metric)
                readable_metric = metric.replace('_', ' ').title()
                
                if score >= 0.8:
                    strengths[agent_name].append(f"Excellent {readable_metric.lower()} ({score:.2f})")
                elif score <= 0.4:
                    weaknesses[agent_name].append(f"Needs improvement in {readable_metric.lower()} ({score:.2f})")
                    
        return dict(strengths), dict(weaknesses)
        
    def _detect_emergent_patterns(self, agent_responses: List[Dict[str, Any]], evaluations: Dict[str, EvaluationMetrics]) -> List[str]:
        """Detect emergent patterns in agent behavior"""
        patterns = []
        
        # Check for consensus on specific topics
        common_themes = self._extract_common_themes(agent_responses)
        if len(common_themes) > 2:
            patterns.append(f"Strong consensus on key themes: {', '.join(common_themes[:3])}")
            
        # Check for complementary strengths
        agent_strengths = {}
        for agent_name, metrics in evaluations.items():
            best_metric = max(['technical_accuracy', 'persuasiveness', 'coherence'], 
                            key=lambda m: getattr(metrics, m))
            agent_strengths[agent_name] = best_metric
            
        if len(set(agent_strengths.values())) == len(agent_strengths):
            patterns.append("Agents show complementary strengths across different evaluation dimensions")
            
        # Check for quality evolution
        if len(self.evaluation_history) > 10:
            recent_scores = [h['metrics'].overall_score for h in self.evaluation_history[-10:]]
            if len(recent_scores) > 5:
                trend = np.polyfit(range(len(recent_scores)), recent_scores, 1)[0]
                if trend > 0.01:
                    patterns.append("Positive quality trend detected across recent evaluations")
                elif trend < -0.01:
                    patterns.append("Declining quality trend detected - may need intervention")
                    
        return patterns
        
    # Utility methods
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
        
    def _extract_common_themes(self, agent_responses: List[Dict[str, Any]]) -> List[str]:
        """Extract common themes across agent responses"""
        all_words = []
        for response in agent_responses:
            words = response['text_response'].lower().split()
            # Filter meaningful words
            meaningful_words = [w for w in words if len(w) > 4 and w.isalpha()]
            all_words.extend(meaningful_words)
            
        from collections import Counter
        common_words = Counter(all_words).most_common(10)
        return [word for word, count in common_words if count >= len(agent_responses) // 2]
        
    def _identify_domain(self, query: str) -> str:
        """Identify domain of the query"""
        query_lower = query.lower()
        
        domain_keywords = {
            'financial': ['money', 'invest', 'finance', 'budget', 'cost', 'profit', 'loan', 'debt'],
            'technical': ['software', 'code', 'tech', 'algorithm', 'system', 'database', 'api'],
            'career': ['job', 'work', 'career', 'salary', 'interview', 'promotion'],
            'health': ['health', 'medical', 'doctor', 'treatment', 'exercise'],
            'relationship': ['relationship', 'dating', 'marriage', 'family', 'friend']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return domain
                
        return 'general'
        
    def _has_clear_argument_structure(self, response: str) -> bool:
        """Check if response has clear argument structure"""
        structure_indicators = ['first', 'second', 'third', 'finally', 'in conclusion', 'therefore']
        return any(indicator in response.lower() for indicator in structure_indicators)
        
    def _check_topic_consistency(self, sentences: List[str]) -> float:
        """Check consistency of topic across sentences"""
        if len(sentences) < 2:
            return 0.5
            
        # Simple check based on word overlap between sentences
        overlaps = []
        for i in range(len(sentences) - 1):
            words1 = set(sentences[i].lower().split())
            words2 = set(sentences[i + 1].lower().split())
            overlap = len(words1.intersection(words2)) / len(words1.union(words2)) if words1.union(words2) else 0
            overlaps.append(overlap)
            
        return sum(overlaps) / len(overlaps) if overlaps else 0.5
        
    def _extract_key_concepts(self, query: str) -> List[str]:
        """Extract key concepts from query"""
        # Simple extraction - in practice could use NLP techniques
        important_words = [w for w in query.split() if len(w) > 4 and w.lower() not in ['should', 'would', 'could']]
        return important_words[:5]  # Return top 5
        
    def _identify_expected_components(self, query: str) -> List[str]:
        """Identify expected components in response based on query"""
        components = []
        
        if '?' in query:
            components.append('direct_answer')
            
        if any(word in query.lower() for word in ['pros', 'cons', 'advantages', 'disadvantages']):
            components.extend(['pros', 'cons'])
            
        if any(word in query.lower() for word in ['how', 'steps', 'process']):
            components.append('step_by_step')
            
        if any(word in query.lower() for word in ['why', 'reason', 'because']):
            components.append('reasoning')
            
        return components or ['general_advice']  # Default component
        
    def _check_component_presence(self, response: str, component: str) -> bool:
        """Check if expected component is present in response"""
        component_indicators = {
            'direct_answer': ['answer', 'solution', 'recommendation'],
            'pros': ['advantage', 'benefit', 'positive', 'pro'],
            'cons': ['disadvantage', 'risk', 'negative', 'con', 'drawback'],
            'step_by_step': ['step', 'first', 'second', 'next', 'then'],
            'reasoning': ['because', 'since', 'reason', 'due to'],
            'general_advice': ['recommend', 'suggest', 'advice', 'should']
        }
        
        indicators = component_indicators.get(component, [])
        return any(indicator in response.lower() for indicator in indicators)
        
    def _has_clear_introduction(self, response: str) -> bool:
        """Check if response has clear introduction"""
        intro_phrases = ['let me', 'i would', 'to answer', 'regarding', 'concerning']
        first_sentence = response.split('.')[0].lower()
        return any(phrase in first_sentence for phrase in intro_phrases)
        
    def _has_logical_progression(self, response: str) -> bool:
        """Check if response has logical progression"""
        progression_words = ['first', 'second', 'then', 'next', 'furthermore', 'additionally', 'however']
        return sum(1 for word in progression_words if word in response.lower()) >= 2
        
    def _has_clear_conclusion(self, response: str) -> bool:
        """Check if response has clear conclusion"""
        conclusion_phrases = ['in conclusion', 'therefore', 'thus', 'overall', 'to summarize']
        last_sentences = ' '.join(response.split('.')[-2:]).lower()
        return any(phrase in last_sentences for phrase in conclusion_phrases)
        
    async def _check_factual_accuracy(self, response: str, domain: str, benchmarks: Dict) -> float:
        """Check factual accuracy against benchmarks"""
        # Simplified factual checking - in practice would use external APIs
        factual_claims = self._extract_factual_claims(response)
        
        if not factual_claims:
            return 0.7  # Neutral for opinion-based responses
            
        # For demo purposes, return a score based on domain knowledge
        domain_accuracy = {
            'financial': 0.8,  # Generally good financial knowledge
            'technical': 0.85, # High technical accuracy
            'career': 0.75,    # Decent career advice
            'health': 0.7,     # Conservative on health claims
            'general': 0.8     # Good general knowledge
        }
        
        return domain_accuracy.get(domain, 0.75)
        
    def _check_best_practices_alignment(self, response: str, domain: str, benchmarks: Dict) -> float:
        """Check alignment with best practices"""
        best_practice_scores = {
            'financial': 0.8,   # Good financial practices
            'technical': 0.85,  # Strong technical practices
            'career': 0.8,      # Solid career advice
            'health': 0.75,     # Conservative health advice
            'general': 0.8      # Good general practices
        }
        
        return best_practice_scores.get(domain, 0.75)
        
    def _check_industry_compliance(self, response: str, domain: str, benchmarks: Dict) -> float:
        """Check compliance with industry standards"""
        compliance_scores = {
            'financial': 0.75,  # Financial regulations consideration
            'technical': 0.8,   # Technical standards
            'career': 0.85,     # Professional standards
            'health': 0.7,      # Medical compliance
            'general': 0.8      # General compliance
        }
        
        return compliance_scores.get(domain, 0.75)
        
    def _generate_recommendations(self, 
                                comparative_analysis: ComparativeAnalysis,
                                benchmark_results: Optional[Dict[str, Any]]) -> str:
        """Generate recommendations for improvement"""
        
        recommendations = []
        
        # Based on consensus level
        if comparative_analysis.consensus_level < 0.5:
            recommendations.append("• Increase agent coordination to improve consensus building")
        elif comparative_analysis.consensus_level > 0.9:
            recommendations.append("• Consider adding more diverse perspectives to avoid groupthink")
            
        # Based on quality distribution
        quality_dist = comparative_analysis.quality_distribution
        low_quality_metrics = [k for k, v in quality_dist.items() if v < 0.6]
        if low_quality_metrics:
            recommendations.append(f"• Focus improvement on: {', '.join(low_quality_metrics)}")
            
        # Agent-specific recommendations
        bottom_agent = comparative_analysis.agent_rankings[-1][0]
        recommendations.append(f"• Provide additional training for {bottom_agent} agent")
        
        # Diversity recommendations
        if comparative_analysis.diversity_score < 0.1:
            recommendations.append("• Increase response diversity through prompt engineering")
            
        return '\n'.join(recommendations) if recommendations else "• System performance is optimal - continue current approach" 
/**
 * API client for the Agentic Math System
 */

import axios, { AxiosInstance } from 'axios'
import { MathItem, AgentType, EvaluationResult, SkillId, Difficulty, SeedCase } from '@/types/agentic'

class AgenticApiClient {
  private client: AxiosInstance

  constructor() {
    const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await this.client.get('/health')
    return response.data
  }

  // Generate item using engine
  async generateItem(
    skillId: SkillId, 
    difficulty?: Difficulty, 
    seed?: number
  ): Promise<MathItem> {
    const response = await this.client.post('/items/generate', {
      skill_id: skillId,
      difficulty,
      seed,
      mode: 'random'
    })
    return response.data
  }

  // Grade item response
  async gradeItem(
    item: MathItem, 
    choiceId: string
  ): Promise<{ correct: boolean; solution_choice_id: string; explanation: string }> {
    const response = await this.client.post('/grade', {
      item,
      choice_id: choiceId
    })
    return response.data
  }

  // Get skills manifest (template counts)
  async getSkillsManifest(): Promise<Record<SkillId, Record<Difficulty, number>>> {
    const response = await this.client.get('/skills/manifest')
    return response.data
  }

  // Run agent evaluation (we'll need to add this to the backend)
  async runAgentEvaluation(agent: AgentType): Promise<EvaluationResult[]> {
    // For now, simulate the evaluation data
    // TODO: Implement actual backend endpoint
    return this.mockEvaluationResults(agent)
  }

  // Run single agent test
  async testAgent(
    agent: AgentType,
    item: MathItem
  ): Promise<{ choice: string; correct: boolean; reasoning?: string }> {
    // TODO: Implement actual agent testing endpoint
    // For now, simulate agent behavior
    return this.mockAgentTest(agent, item)
  }

  // Get seed cases
  async getSeedCases(): Promise<SeedCase[]> {
    // TODO: Implement endpoint to fetch seed cases
    return this.mockSeedCases()
  }

  // Mock implementations (to be replaced with real endpoints)
  private async mockEvaluationResults(agent: AgentType): Promise<EvaluationResult[]> {
    // Simulate evaluation results based on our actual data
    const mockResults: EvaluationResult[] = [
      {
        id: 'vtx-1',
        agent,
        skill_id: 'quad.graph.vertex',
        difficulty: 'easy',
        seed: 42,
        status: 'ok',
        ok: true,
        picked: 'D',
        solution: 'D',
        gen_ms: 2,
        grade_ms: 1,
        stem_hash: 'ce7c7133df',
        error: null
      },
      // Add more mock results...
    ]
    
    return mockResults
  }

  private async mockAgentTest(
    agent: AgentType, 
    item: MathItem
  ): Promise<{ choice: string; correct: boolean; reasoning?: string }> {
    // Simulate agent behavior
    const choices = ['A', 'B', 'C', 'D']
    const randomChoice = choices[Math.floor(Math.random() * choices.length)]
    
    return {
      choice: randomChoice,
      correct: randomChoice === item.solution_choice_id,
      reasoning: `${agent} agent selected ${randomChoice}`
    }
  }

  private mockSeedCases(): SeedCase[] {
    return [
      { id: 'vtx-1', skill_id: 'quad.graph.vertex', difficulty: 'easy', seed: 42 },
      { id: 'std-1', skill_id: 'quad.standard.vertex', difficulty: 'easy', seed: 11 },
      // Add more seed cases...
    ]
  }
}

export const api = new AgenticApiClient()
export default api
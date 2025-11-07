'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { 
  BeakerIcon, 
  ChartBarIcon, 
  CogIcon, 
  DocumentTextIcon,
  PlayIcon,
  StarIcon
} from '@heroicons/react/24/outline'
import { getAllSkills, getTotalTemplates, AGENT_DEFINITIONS } from '@/lib/skills'
import { api } from '@/lib/api'

export default function HomePage() {
  const [stats, setStats] = useState({
    totalSkills: 9,
    totalTemplates: 71,
    totalSeedCases: 36,
    lastAccuracy: 69.44
  })
  
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null)

  useEffect(() => {
    // Check API health
    api.healthCheck()
      .then(() => setIsHealthy(true))
      .catch(() => setIsHealthy(false))
  }, [])

  const features = [
    {
      name: 'Agent Playground',
      description: 'Test and compare rule-based agents interactively',
      icon: PlayIcon,
      href: '/playground',
      color: 'bg-blue-500'
    },
    {
      name: 'Skill Explorer',
      description: 'Browse 9 quadratic skills with 71 templates',
      icon: DocumentTextIcon,
      href: '/skills',
      color: 'bg-green-500'
    },
    {
      name: 'Evaluation Center',
      description: 'Run comprehensive agent evaluations',
      icon: BeakerIcon,
      href: '/evaluation',
      color: 'bg-purple-500'
    },
    {
      name: 'Performance Analytics',
      description: 'View agent performance metrics and trends',
      icon: ChartBarIcon,
      href: '/analytics',
      color: 'bg-orange-500'
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
                  <CogIcon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">Agentic Math System</h1>
                  <p className="text-sm text-gray-500">Rule-Based Quadratic Agents</p>
                </div>
              </div>
            </div>
            
            {/* API Status */}
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${
                isHealthy === true ? 'bg-green-500' : 
                isHealthy === false ? 'bg-red-500' : 'bg-yellow-500'
              }`} />
              <span className="text-sm text-gray-600">
                API {isHealthy === true ? 'Online' : isHealthy === false ? 'Offline' : 'Checking...'}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 sm:text-5xl mb-4">
            Mathematical Intelligence
            <span className="block text-blue-600">Through Rule-Based Agents</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            Explore our comprehensive system of 9 quadratic skills powered by deterministic 
            rule-based agents with 69% accuracy across 36 evaluation cases.
          </p>
          
          {/* Quick Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto mb-12">
            <div className="bg-white rounded-lg p-4 shadow-sm border">
              <div className="text-2xl font-bold text-blue-600">{stats.totalSkills}</div>
              <div className="text-sm text-gray-600">Quadratic Skills</div>
            </div>
            <div className="bg-white rounded-lg p-4 shadow-sm border">
              <div className="text-2xl font-bold text-green-600">{stats.totalTemplates}</div>
              <div className="text-sm text-gray-600">Math Templates</div>
            </div>
            <div className="bg-white rounded-lg p-4 shadow-sm border">
              <div className="text-2xl font-bold text-purple-600">{stats.totalSeedCases}</div>
              <div className="text-sm text-gray-600">Evaluation Cases</div>
            </div>
            <div className="bg-white rounded-lg p-4 shadow-sm border">
              <div className="text-2xl font-bold text-orange-600">{stats.lastAccuracy}%</div>
              <div className="text-sm text-gray-600">Rules Accuracy</div>
            </div>
          </div>
        </div>

        {/* Agent Types */}
        <div className="mb-16">
          <h3 className="text-2xl font-bold text-gray-900 text-center mb-8">Available Agents</h3>
          <div className="grid md:grid-cols-3 gap-6">
            {Object.entries(AGENT_DEFINITIONS).map(([key, agent]) => (
              <div key={key} className="bg-white rounded-lg p-6 shadow-sm border hover:shadow-md transition-shadow">
                <div className="flex items-center mb-4">
                  <div className={`w-4 h-4 rounded-full ${agent.color} mr-3`} />
                  <h4 className="text-lg font-semibold text-gray-900">{agent.name}</h4>
                </div>
                <p className="text-gray-600">{agent.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Feature Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {features.map((feature, index) => (
            <Link
              key={feature.name}
              href={feature.href}
              className="group block"
            >
              <div className="bg-white rounded-lg p-6 shadow-sm border hover:shadow-lg transition-all duration-200 group-hover:border-blue-300">
                <div className={`w-12 h-12 ${feature.color} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.name}</h3>
                <p className="text-gray-600 text-sm">{feature.description}</p>
              </div>
            </Link>
          ))}
        </div>

        {/* Call to Action */}
        <div className="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-2xl p-8 text-center text-white">
          <h3 className="text-2xl font-bold mb-4">Start Exploring</h3>
          <p className="text-blue-100 mb-6 max-w-2xl mx-auto">
            Dive into our agent playground to test mathematical reasoning, 
            or explore the skill matrix to understand our comprehensive quadratic coverage.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/playground"
              className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors inline-flex items-center justify-center"
            >
              <PlayIcon className="w-5 h-5 mr-2" />
              Try Agent Playground
            </Link>
            <Link
              href="/skills"
              className="border border-blue-300 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-600 transition-colors inline-flex items-center justify-center"
            >
              <DocumentTextIcon className="w-5 h-5 mr-2" />
              Browse Skills
            </Link>
          </div>
        </div>
      </main>
    </div>
  )
}
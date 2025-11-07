'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { 
  ArrowLeftIcon,
  DocumentTextIcon,
  ChartBarIcon,
  BeakerIcon
} from '@heroicons/react/24/outline'
import { SkillId, Difficulty } from '@/types/agentic'
import { SKILL_DEFINITIONS, DIFFICULTY_DEFINITIONS, getAllSkills } from '@/lib/skills'
import { api } from '@/lib/api'

export default function SkillsPage() {
  const [skillsManifest, setSkillsManifest] = useState<Record<SkillId, Record<Difficulty, number>> | null>(null)
  const [selectedSkill, setSelectedSkill] = useState<SkillId | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadManifest = async () => {
      try {
        const manifest = await api.getSkillsManifest()
        setSkillsManifest(manifest)
      } catch (error) {
        console.error('Error loading skills manifest:', error)
      } finally {
        setLoading(false)
      }
    }

    loadManifest()
  }, [])

  const skills = getAllSkills()

  const getTemplateCount = (skillId: SkillId, difficulty?: Difficulty) => {
    if (!skillsManifest) return 0
    if (difficulty) {
      return skillsManifest[skillId]?.[difficulty] || 0
    }
    return Object.values(skillsManifest[skillId] || {}).reduce((sum, count) => sum + count, 0)
  }

  const getTotalTemplates = () => {
    if (!skillsManifest) return 0
    return Object.values(skillsManifest).reduce((total, difficulties) => 
      total + Object.values(difficulties).reduce((sum, count) => sum + count, 0), 0
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-4">
            <div className="flex items-center space-x-4">
              <Link href="/" className="text-gray-500 hover:text-gray-700">
                <ArrowLeftIcon className="w-6 h-6" />
              </Link>
              <div className="flex items-center space-x-3">
                <DocumentTextIcon className="w-6 h-6 text-green-600" />
                <h1 className="text-xl font-semibold text-gray-900">Skill Explorer</h1>
              </div>
            </div>
            <div className="text-sm text-gray-600">
              {getTotalTemplates()} Total Templates
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-gray-600">Loading skills...</span>
          </div>
        ) : (
          <div className="grid lg:grid-cols-4 gap-8">
            {/* Skills List */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-sm border p-6 sticky top-8">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  Quadratic Skills ({skills.length})
                </h2>
                <div className="space-y-2">
                  {skills.map((skill) => (
                    <button
                      key={skill.id}
                      onClick={() => setSelectedSkill(skill.id)}
                      className={`w-full text-left p-3 rounded-lg border transition-colors ${
                        selectedSkill === skill.id
                          ? 'bg-blue-50 border-blue-200 text-blue-700'
                          : 'bg-gray-50 border-gray-200 text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <div className="font-medium text-sm">{skill.name}</div>
                      <div className="text-xs text-gray-500 mt-1">
                        {getTemplateCount(skill.id)} templates
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Skills Grid */}
            <div className="lg:col-span-3">
              {selectedSkill ? (
                <SkillDetail 
                  skill={SKILL_DEFINITIONS[selectedSkill]}
                  getTemplateCount={getTemplateCount}
                />
              ) : (
                <SkillsOverview 
                  skills={skills}
                  getTemplateCount={getTemplateCount}
                  onSelectSkill={setSelectedSkill}
                />
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

function SkillsOverview({ 
  skills, 
  getTemplateCount, 
  onSelectSkill 
}: {
  skills: typeof SKILL_DEFINITIONS[keyof typeof SKILL_DEFINITIONS][]
  getTemplateCount: (skillId: SkillId, difficulty?: Difficulty) => number
  onSelectSkill: (skillId: SkillId) => void
}) {
  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">All Quadratic Skills</h2>
        <p className="text-gray-600">
          Comprehensive coverage of quadratic mathematics through 9 specialized skills.
          Each skill includes templates across 4 difficulty levels.
        </p>
      </div>

      <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-6">
        {skills.map((skill) => (
          <div
            key={skill.id}
            onClick={() => onSelectSkill(skill.id)}
            className="skill-card cursor-pointer"
          >
            <div className="flex items-start justify-between mb-3">
              <h3 className="font-semibold text-gray-900 text-sm">{skill.name}</h3>
              <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded">
                {getTemplateCount(skill.id)}
              </span>
            </div>
            <p className="text-gray-600 text-sm mb-4">{skill.description}</p>
            
            <div className="flex flex-wrap gap-1">
              {(['easy', 'medium', 'hard', 'applied'] as Difficulty[]).map((difficulty) => (
                <span
                  key={difficulty}
                  className={`text-xs px-2 py-1 rounded ${DIFFICULTY_DEFINITIONS[difficulty].color}`}
                >
                  {difficulty}: {getTemplateCount(skill.id, difficulty)}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function SkillDetail({ 
  skill, 
  getTemplateCount 
}: {
  skill: typeof SKILL_DEFINITIONS[keyof typeof SKILL_DEFINITIONS]
  getTemplateCount: (skillId: SkillId, difficulty?: Difficulty) => number
}) {
  const difficulties: Difficulty[] = ['easy', 'medium', 'hard', 'applied']
  
  return (
    <div>
      {/* Skill Header */}
      <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">{skill.name}</h2>
            <p className="text-gray-600">{skill.description}</p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-blue-600">
              {getTemplateCount(skill.id)}
            </div>
            <div className="text-sm text-gray-500">Total Templates</div>
          </div>
        </div>

        {/* Difficulty Breakdown */}
        <div className="grid grid-cols-4 gap-4">
          {difficulties.map((difficulty) => (
            <div key={difficulty} className="text-center">
              <div className={`p-3 rounded-lg ${DIFFICULTY_DEFINITIONS[difficulty].color}`}>
                <div className="font-semibold">
                  {getTemplateCount(skill.id, difficulty)}
                </div>
                <div className="text-xs capitalize">
                  {difficulty}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="grid md:grid-cols-2 gap-4">
        <Link
          href={`/playground?skill=${skill.id}`}
          className="bg-white rounded-lg shadow-sm border p-6 hover:shadow-md transition-shadow group"
        >
          <div className="flex items-center space-x-3">
            <BeakerIcon className="w-8 h-8 text-blue-600 group-hover:scale-110 transition-transform" />
            <div>
              <h3 className="font-semibold text-gray-900">Test in Playground</h3>
              <p className="text-sm text-gray-600">Try agents on this skill</p>
            </div>
          </div>
        </Link>

        <Link
          href={`/analytics?skill=${skill.id}`}
          className="bg-white rounded-lg shadow-sm border p-6 hover:shadow-md transition-shadow group"
        >
          <div className="flex items-center space-x-3">
            <ChartBarIcon className="w-8 h-8 text-green-600 group-hover:scale-110 transition-transform" />
            <div>
              <h3 className="font-semibold text-gray-900">View Analytics</h3>
              <p className="text-sm text-gray-600">Performance metrics</p>
            </div>
          </div>
        </Link>
      </div>

      {/* Skill ID */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <div className="text-sm text-gray-600">
          <strong>Skill ID:</strong> <code className="bg-white px-2 py-1 rounded border">{skill.id}</code>
        </div>
      </div>
    </div>
  )
}
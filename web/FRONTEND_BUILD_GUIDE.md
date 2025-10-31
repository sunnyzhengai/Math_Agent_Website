# Frontend Build Guide - Next.js Components

This guide outlines the remaining work to complete the Math Agent frontend.

## ✅ Done

- [x] Next.js 14 scaffold with App Router
- [x] TypeScript configuration
- [x] Tailwind CSS setup
- [x] API types matching backend
- [x] Project structure

## ⏳ TODO - Priority Order

### Phase 1: Core Infrastructure (2-3 hours)

#### 1.1 API Client (`lib/api.ts`)

```typescript
import axios from 'axios'

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Export methods
export const api = {
  nextItem: (userId: string, domain: string = 'Quadratics', seed?: number) =>
    apiClient.post('/next-item', { user_id: userId, domain, seed }),
  
  grade: (userId: string, itemId: string, choiceId: string, timeMs: number, confidence: number) =>
    apiClient.post('/grade', {
      user_id: userId,
      item_id: itemId,
      selected_choice_id: choiceId,
      time_ms: timeMs,
      confidence,
    }),
  
  progress: (userId: string, domain: string = 'Quadratics') =>
    apiClient.get('/progress', { params: { user_id: userId, domain } }),
  
  skills: (domain: string = 'Quadratics') =>
    apiClient.get('/skills', { params: { domain } }),
}

export default apiClient
```

#### 1.2 State Management (`lib/store.ts`)

```typescript
import { create } from 'zustand'
import { Item, SkillProgress, UserSession } from '@/types/api'

interface AppState {
  user: UserSession | null
  currentItem: Item | null
  selectedChoice: string | null
  feedback: { correct: boolean; tags: string[] } | null
  mastery: number
  skills: SkillProgress[]
  
  // Actions
  setUser: (user: UserSession | null) => void
  setCurrentItem: (item: Item) => void
  selectChoice: (choiceId: string) => void
  setFeedback: (feedback: AppState['feedback']) => void
  updateMastery: (mastery: number) => void
  setSkills: (skills: SkillProgress[]) => void
  reset: () => void
}

export const useAppStore = create<AppState>((set) => ({
  user: null,
  currentItem: null,
  selectedChoice: null,
  feedback: null,
  mastery: 0.5,
  skills: [],
  
  setUser: (user) => set({ user }),
  setCurrentItem: (item) => set({ currentItem: item }),
  selectChoice: (choiceId) => set({ selectedChoice: choiceId }),
  setFeedback: (feedback) => set({ feedback }),
  updateMastery: (mastery) => set({ mastery }),
  setSkills: (skills) => set({ skills }),
  reset: () => set({
    currentItem: null,
    selectedChoice: null,
    feedback: null,
  }),
}))
```

#### 1.3 Auth Helper (`lib/auth.ts`)

```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_KEY!
)

export const authHelpers = {
  signUp: (email: string, password: string) =>
    supabase.auth.signUp({ email, password }),
  
  signIn: (email: string, password: string) =>
    supabase.auth.signInWithPassword({ email, password }),
  
  signOut: () => supabase.auth.signOut(),
  
  getCurrentUser: () => supabase.auth.getUser(),
  
  resetPassword: (email: string) =>
    supabase.auth.resetPasswordForEmail(email),
}

export default supabase
```

### Phase 2: Layouts & Pages (3-4 hours)

#### 2.1 Root Layout (`app/layout.tsx`)

```typescript
import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Math Agent - Quadratics Mastery',
  description: 'Interactive skill-based learning platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        <div className="min-h-screen flex flex-col">
          {/* Header */}
          {/* Main content */}
          <main className="flex-1">{children}</main>
          {/* Footer */}
        </div>
      </body>
    </html>
  )
}
```

#### 2.2 Landing Page (`app/page.tsx`)

- Hero section with CTA
- Feature highlights
- Call-to-action buttons
- Responsive layout

#### 2.3 Auth Pages

- `app/auth/signup/page.tsx` - Sign up form
- `app/auth/login/page.tsx` - Login form
- `app/auth/reset/page.tsx` - Password reset

#### 2.4 Student App (`app/app/page.tsx`)

- Get next item on load
- Display question with choices
- Track time spent
- Show feedback after submission
- Display mastery progress

#### 2.5 Teacher Dashboard (`app/dashboard/page.tsx`)

- List all students
- Show skills mastery heatmap
- Display misconception stats
- Weekly accuracy chart

### Phase 3: Components (4-5 hours)

#### 3.1 Core Components

```
components/
├── Header.tsx              # Navigation bar
├── Footer.tsx              # Footer
├── Button.tsx              # Reusable button
├── Card.tsx                # Card container
├── Question.tsx            # Question display
├── ChoiceButton.tsx        # Choice option
├── FeedbackCard.tsx        # Show correct/wrong
├── ProgressBar.tsx         # Mastery visualizer
├── SkillCard.tsx           # Skill progress
├── Timer.tsx               # Question timer
├── MiniLesson.tsx          # Resource drawer
└── Heatmap.tsx             # Misconception matrix
```

#### Example: Question Component

```typescript
'use client'

import { Item } from '@/types/api'
import ChoiceButton from './ChoiceButton'
import Timer from './Timer'

interface QuestionProps {
  item: Item
  onSelect: (choiceId: string) => void
  onSubmit: () => void
  selectedChoice: string | null
}

export default function Question({
  item,
  onSelect,
  onSubmit,
  selectedChoice,
}: QuestionProps) {
  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow">
      <Timer duration={300} />
      
      <h2 className="text-2xl font-bold mb-4">{item.stem}</h2>
      
      <div className="space-y-3 mb-6">
        {item.choices.map((choice) => (
          <ChoiceButton
            key={choice.id}
            choice={choice}
            selected={selectedChoice === choice.id}
            onClick={() => onSelect(choice.id)}
          />
        ))}
      </div>
      
      <button
        onClick={onSubmit}
        disabled={!selectedChoice}
        className="w-full bg-blue-600 text-white py-2 rounded-lg disabled:opacity-50"
      >
        Submit Answer
      </button>
    </div>
  )
}
```

### Phase 4: Integration (2-3 hours)

#### 4.1 Connect to Backend

- Import `api` client in pages
- Call `/next-item` on load
- Call `/grade` on submission
- Fetch `/progress` for dashboard
- Handle loading/error states

#### 4.2 Auth Flow

- Protect `/app` and `/dashboard` routes
- Redirect to `/auth/login` if not authenticated
- Store JWT in localStorage
- Pass token in API requests

#### 4.3 State Management

- Use `useAppStore` for global state
- Persist user session
- Cache API responses

### Phase 5: Polish (1-2 hours)

#### 5.1 UX Enhancements

- Loading states with spinners
- Error boundaries
- Toast notifications
- Skeleton screens
- Responsive design for mobile

#### 5.2 Styling

- Create `styles/globals.css`
- Define color palette
- Utility classes
- Dark mode (optional)

#### 5.3 Accessibility

- ARIA labels
- Keyboard navigation
- Focus states
- Color contrast

---

## Development Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev
# → http://localhost:3000

# Type checking
npm run type-check

# Linting
npm run lint

# Production build
npm run build

# Start production server
npm start
```

---

## Environment Setup

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_KEY=your_anon_key
```

---

## Deployment to Vercel

1. Connect GitHub repo to Vercel
2. Select `/web` as root directory
3. Add environment variables
4. Deploy!

---

## Testing

```bash
# Run tests (setup jest + testing-library)
npm test

# E2E tests (setup playwright)
npm run e2e
```

---

## Estimated Timeline

| Task | Hours |
|------|-------|
| API & Auth Setup | 2-3 |
| Layouts & Pages | 3-4 |
| Components | 4-5 |
| Integration | 2-3 |
| Polish & Deploy | 2-3 |
| **TOTAL** | **13-18** |

---

## Next: Pick a Component

Want me to build one of these next?

1. **API Client** (`lib/api.ts`) - 30 min
2. **Question Component** (`components/Question.tsx`) - 1 hour
3. **Landing Page** (`app/page.tsx`) - 1 hour
4. **Auth Login** (`app/auth/login/page.tsx`) - 1 hour
5. **Student App** (`app/app/page.tsx`) - 2 hours

Which would you like? 🚀

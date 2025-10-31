# Math Agent - Next.js Frontend

Beautiful, responsive web interface for Quadratics skill mastery platform.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Custom + shadcn/ui (coming)
- **Auth**: Supabase
- **HTTP**: Axios
- **State**: Zustand
- **Build**: Vercel

## Getting Started

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_KEY=your_anon_key
```

### 3. Run Development Server

```bash
npm run dev
# → http://localhost:3000
```

## Project Structure

```
web/
├── app/              # Next.js App Router
│   ├── page.tsx      # Landing page
│   ├── app/          # Student learning interface
│   ├── dashboard/    # Teacher dashboard
│   ├── auth/         # Auth pages
│   └── layout.tsx    # Root layout
├── components/       # Reusable React components
│   ├── Question.tsx
│   ├── SkillCard.tsx
│   ├── ProgressBar.tsx
│   └── ...
├── lib/             # Utilities
│   ├── api.ts       # API client (axios)
│   ├── auth.ts      # Supabase auth
│   └── store.ts     # State management (Zustand)
├── types/           # TypeScript interfaces
│   └── api.ts       # API types
└── styles/          # Global styles
    └── globals.css
```

## Key Features

### Landing Page
- Project overview
- Call-to-action (Start Learning)
- Responsive design

### Student App (`/app`)
- Question display with 4 choices
- Timer + confidence slider
- Instant feedback (correct/wrong)
- Mastery progress bar
- Mini-lesson drawer with resources
- "Why this next?" explanation

### Teacher Dashboard (`/dashboard`)
- Skills grid with mastery %
- Misconception heatmap
- Weekly accuracy chart
- "Due today" list
- Student progress over time

### Authentication
- Sign up / Login with Supabase
- Email verification
- Password reset
- User profile management
- Role-based access (student/teacher)

## API Integration

All endpoints call the FastAPI backend (`http://localhost:8000`):

```typescript
// Example: Get next question
const response = await apiClient.post('/next-item', {
  user_id: 'julia_001',
  domain: 'Quadratics',
})

// Example: Submit answer
const result = await apiClient.post('/grade', {
  user_id: 'julia_001',
  item_id: 'item_123',
  selected_choice_id: 'c1',
  time_ms: 5000,
  confidence: 0.8,
})
```

## Development Workflow

1. **Create a new component** in `components/`
2. **Use TypeScript types** from `types/api.ts`
3. **Test locally**: `npm run dev`
4. **Check types**: `npm run type-check`
5. **Lint**: `npm run lint`

## Deployment

### Vercel (Recommended)

1. Connect GitHub repo
2. Select `/web` as root directory
3. Add environment variables:
   - `NEXT_PUBLIC_API_URL=https://api.mathagent.app`
   - `NEXT_PUBLIC_SUPABASE_URL=...`
   - `NEXT_PUBLIC_SUPABASE_KEY=...`
4. Deploy!

## Building

```bash
# Production build
npm run build

# Start production server
npm start
```

## Next Steps

- [ ] Create API client (`lib/api.ts`)
- [ ] Set up Supabase auth (`lib/auth.ts`)
- [ ] Create state management (`lib/store.ts`)
- [ ] Build landing page component
- [ ] Build question card component
- [ ] Build progress dashboard
- [ ] Connect to FastAPI backend
- [ ] Deploy to Vercel

## Resources

- [Next.js Docs](https://nextjs.org)
- [Tailwind Docs](https://tailwindcss.com)
- [Supabase Docs](https://supabase.com/docs)
- [Axios Docs](https://axios-http.com)

export type UserRole = 
  | 'SUPER_ADMIN'
  | 'PLATFORM_ADMIN'
  | 'ORGANIZATION_ADMIN'
  | 'TEACHER'
  | 'TEACHING_ASSISTANT'
  | 'STUDENT'
  | 'MODERATOR'
  | 'SUPPORT_AGENT';

export interface UserProfile {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  avatarUrl?: string;
  bio?: string;
  role: UserRole;
  organizationId?: string;
  organizationName?: string;
  permissions: string[];
}

export interface AuthState {
  user: UserProfile | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface Course {
  id: string;
  title: string;
  slug: string;
  shortDescription: string;
  description: string;
  thumbnailUrl: string;
  category: string;
  difficulty: 'BEGINNER' | 'INTERMEDIATE' | 'ADVANCED';
  durationMinutes: number;
  price: number;
  currency: string;
  instructorName: string;
  instructorAvatar?: string;
  status: 'DRAFT' | 'IN_REVIEW' | 'PUBLISHED' | 'ARCHIVED';
  rating: number;
  enrolledCount: number;
  sectionsCount: number;
  lessonsCount: number;
}

export interface Section {
  id: string;
  title: string;
  description?: string;
  sequenceOrder: number;
  lessons: Lesson[];
}

export interface Lesson {
  id: string;
  sectionId: string;
  title: string;
  lessonType: 'VIDEO' | 'PDF' | 'TEXT' | 'QUIZ' | 'ASSIGNMENT';
  durationSeconds: number;
  sequenceOrder: number;
  isCompleted?: boolean;
  contentBody?: string;
  mediaUrl?: string;
  isFreePreview?: boolean;
}

export interface AiChatMessage {
  id: string;
  senderType: 'USER' | 'AI' | 'SYSTEM';
  content: string;
  citations?: string[];
  createdAt: string;
  isStreaming?: boolean;
}

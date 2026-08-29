import React from "react";
import { mockCourses } from "../../services/api";
import { Card } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { formatCurrency, formatDuration } from "../../lib/utils";
import { Clock, Star, Users } from "lucide-react";
import { useNavigate } from "react-router-dom";

export const CourseCatalogPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white">Explore Course Catalog</h1>
        <p className="text-sm text-slate-400">Curated enterprise courses with AI-grounded tutoring</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockCourses.map((course) => (
          <Card key={course.id} className="flex flex-col justify-between overflow-hidden p-0 border-slate-800">
            <img src={course.thumbnailUrl} alt={course.title} className="h-44 w-full object-cover" />
            <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <Badge variant="primary">{course.category}</Badge>
                  <span className="text-xs font-semibold text-indigo-400">{course.difficulty}</span>
                </div>
                <h3 className="font-semibold text-white text-base line-clamp-2">{course.title}</h3>
                <p className="text-xs text-slate-400 mt-2 line-clamp-2">{course.shortDescription}</p>
              </div>

              <div className="pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                <span className="flex items-center gap-1"><Clock className="h-3.5 w-3.5" /> {formatDuration(course.durationMinutes)}</span>
                <span className="flex items-center gap-1"><Star className="h-3.5 w-3.5 text-amber-400 fill-amber-400" /> {course.rating}</span>
                <span className="text-base font-bold text-white">{formatCurrency(course.price)}</span>
              </div>

              <Button variant="primary" size="sm" onClick={() => navigate(`/learn/${course.id}/lesson-1`)} className="w-full">
                Enroll Now
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

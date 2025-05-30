const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://your-api-url.com';

export async function fetchAttendanceData(params: {
  date: string;
  time_start?: string;
  time_end?: string;
  name?: string;
  min_duration_min?: string;
  max_duration_min?: string;
}) {
  const searchParams = new URLSearchParams();
  
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') {
      searchParams.append(key, value);
    }
  });
  
  const response = await fetch(`${API_BASE_URL}/api/attendance?${searchParams.toString()}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `API error: ${response.status}`);
  }
  
  return response.json();
}

export async function exportAttendanceData(params: {
  date: string;
  time_start?: string;
  time_end?: string;
  name?: string;
  min_duration_min?: string;
  max_duration_min?: string;
  format: 'csv' | 'excel' | 'pdf';
}) {
  const searchParams = new URLSearchParams();
  
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') {
      searchParams.append(key, value);
    }
  });
  
  const response = await fetch(`${API_BASE_URL}/api/attendance/export?${searchParams.toString()}`, {
    method: 'GET',
    headers: {
    },
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `Export error: ${response.status}`);
  }
  
  return response.blob();
}

export async function fetchAttendanceStats(params: {
  date: string;
  time_start?: string;
  time_end?: string;
}) {
  const searchParams = new URLSearchParams();
  
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') {
      searchParams.append(key, value);
    }
  });
  
  const response = await fetch(`${API_BASE_URL}/api/attendance/stats?${searchParams.toString()}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `Stats error: ${response.status}`);
  }
  
  return response.json();
}
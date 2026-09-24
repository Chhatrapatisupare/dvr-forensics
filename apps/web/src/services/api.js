const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8001";

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...(options.headers || {}),
    },
  });

  if (!response.ok) {
    let message = `API request failed: ${response.status}`;

    try {
      const error = await response.json();
      message = error.detail || message;
    } catch {
      // Ignore JSON parsing errors.
    }

    throw new Error(message);
  }

  return response.json();
}

export const api = {
  health: () => request("/api/health"),

  cases: () => request("/api/cases"),

  evidence: () => request("/api/evidence"),

  recordings: (evidenceId) =>
    request(`/api/evidence/${evidenceId}/recordings`),

  timeline: (evidenceId) =>
    request(`/api/evidence/${evidenceId}/timeline`),

  custody: (evidenceId) =>
    request(`/api/evidence/${evidenceId}/custody`),

  verify: (evidenceId) =>
    request(`/api/evidence/${evidenceId}/verify`, {
      method: "POST",
    }),

  provenance: (evidenceId) =>
    request(`/api/evidence/${evidenceId}/provenance`),

  recoveryArtifacts: (evidenceId) =>
    request(`/api/evidence/${evidenceId}/recovery-artifacts`),

  recover: (evidenceId, recordingId) =>
    request(`/api/evidence/${evidenceId}/recover`, {
      method: "POST",
      body: JSON.stringify({
        recording_id: recordingId,
      }),
    }),
};
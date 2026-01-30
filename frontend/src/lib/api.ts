export interface ProcessingResult {
    text: string;
    braille: string;
}

export const processAudio = async (file: Blob): Promise<ProcessingResult> => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://localhost:8000/process-audio", {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to process audio");
    }

    return response.json();
};

"""
Gemini API Handler for AI-based analysis
"""
import google.generativeai as genai
from django.conf import settings
import json


class GeminiHandler:
    """Handler for Gemini API operations"""
    
    def __init__(self, model_name='gemini-2.5-pro'):
        """
        Initialize Gemini handler with specified model
        Available models:
        - gemini-2.5-pro (RECOMMENDED - most capable, stable June 2025)
        - gemini-2.5-flash (fast and efficient)
        - gemini-2.0-flash (older but reliable)
        - gemini-pro-latest (automatically uses latest Pro)
        """
        self.api_key = settings.GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_name)
            self.model_name = model_name
        else:
            self.model = None
            self.model_name = None
    
    def analyze_repository(self, repo_data):
        """
        Analyze repository data using Gemini AI
        Returns AI-generated summary, insights, and suggestions
        """
        if not self.model:
            return {
                "success": False,
                "error": "Gemini API key not configured"
            }
        
        try:
            # Prepare the prompt
            prompt = self._create_analysis_prompt(repo_data)
            
            # Generate content
            response = self.model.generate_content(prompt)
            
            # Parse the response
            analysis = self._parse_analysis_response(response.text)
            
            return {
                "success": True,
                "analysis": analysis,
                "raw_response": response.text
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_analysis_prompt(self, repo_data):
        """
        Create a detailed prompt for Gemini based on repository data
        """
        # Extract relevant information
        commit_count = repo_data.get("commit_count", 0)
        languages = repo_data.get("languages", {})
        readme = repo_data.get("readme_content", "")
        last_commit = repo_data.get("last_commit", {})
        contributors = repo_data.get("contributors", [])
        repo_info = repo_data.get("repo_info", {})
        
        # Calculate language percentages
        total_bytes = sum(languages.values()) if languages else 0
        language_breakdown = ""
        if total_bytes > 0:
            for lang, bytes_count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
                percentage = (bytes_count / total_bytes) * 100
                language_breakdown += f"- {lang}: {percentage:.1f}%\n"
        
        # Format prompt
        prompt = f"""
You are an expert code reviewer and educational mentor. Analyze the following student's GitHub repository and provide constructive feedback.

**Repository Information:**
- Total Commits: {commit_count}
- Languages Used:
{language_breakdown if language_breakdown else "- No language data available"}

**Last Commit:**
- Message: {last_commit.get('message', 'N/A') if last_commit else 'N/A'}
- Date: {last_commit.get('date', 'N/A') if last_commit else 'N/A'}

**Contributors:** {len(contributors)}

**README Excerpt:**
{readme[:500] if readme else "No README available"}

**Project Description:**
{repo_info.get('description', 'No description available')}

---

Please provide a comprehensive analysis in the following format:

**1. Summary (50-75 words):**
Briefly describe what this project does and its overall quality.

**2. Strengths (3-5 points):**
List the positive aspects of this repository.

**3. Areas for Improvement (3-5 points):**
Suggest specific improvements the student could make.

**4. Performance Score (0-100):**
Rate the overall quality of the project considering code activity, documentation, and best practices.

**5. Recommendations:**
Provide 2-3 actionable next steps for the student.

Keep your feedback constructive, encouraging, and educational.
"""
        return prompt
    
    def _parse_analysis_response(self, response_text):
        """
        Parse Gemini's response into structured data
        """
        # Try to extract structured information
        analysis = {
            "summary": "",
            "strengths": [],
            "improvements": [],
            "score": None,
            "recommendations": [],
            "full_text": response_text
        }
        
        try:
            # Simple parsing - look for sections
            sections = response_text.split("**")
            
            for i, section in enumerate(sections):
                section_lower = section.lower()
                
                if "summary" in section_lower and i + 1 < len(sections):
                    analysis["summary"] = sections[i + 1].strip()
                
                elif "strengths" in section_lower and i + 1 < len(sections):
                    strengths_text = sections[i + 1].strip()
                    analysis["strengths"] = [s.strip() for s in strengths_text.split('\n') if s.strip() and (s.strip().startswith('-') or s.strip().startswith('*'))]
                
                elif "improvement" in section_lower and i + 1 < len(sections):
                    improvements_text = sections[i + 1].strip()
                    analysis["improvements"] = [s.strip() for s in improvements_text.split('\n') if s.strip() and (s.strip().startswith('-') or s.strip().startswith('*'))]
                
                elif "score" in section_lower and i + 1 < len(sections):
                    score_text = sections[i + 1].strip()
                    # Try to extract number
                    import re
                    score_match = re.search(r'(\d+)', score_text)
                    if score_match:
                        analysis["score"] = int(score_match.group(1))
                
                elif "recommendation" in section_lower and i + 1 < len(sections):
                    recommendations_text = sections[i + 1].strip()
                    analysis["recommendations"] = [s.strip() for s in recommendations_text.split('\n') if s.strip() and (s.strip().startswith('-') or s.strip().startswith('*'))]
            
        except Exception as e:
            # If parsing fails, just return the full text
            analysis["parse_error"] = str(e)
        
        return analysis
    
    def generate_summary(self, text, max_words=100):
        """
        Generate a concise summary of given text
        """
        if not self.model:
            return "Gemini API not configured"
        
        try:
            prompt = f"Summarize the following text in {max_words} words or less:\n\n{text}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"

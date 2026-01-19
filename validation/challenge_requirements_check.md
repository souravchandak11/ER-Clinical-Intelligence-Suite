# Challenge Requirements Validation

## 1.1 MANDATORY REQUIREMENTS

### HAI-DEF Model Usage (MANDATORY)
- [ ] MedGemma model is used (verify model name in code)
- [ ] Model is NOT just used out-of-box (fine-tuning is required)
- [ ] Fine-tuning code exists and is documented
- [ ] Fine-tuned model checkpoints are saved
- [ ] Model usage is clearly documented in writeup

**VALIDATION COMMAND:**
```bash
# Search for MedGemma usage in codebase
grep -r "medgemma" backend/ --include="*.py" | wc -l
# Should return > 0

# Check for fine-tuning code
ls -la ml/scripts/train_*.py
# Should show training scripts

# Verify model checkpoints exist
ls -la ml/checkpoints/
# Should contain .pth or adapter files
```

### Submission Package Components
- [ ] Video demo exists (3 minutes or less)
- [ ] Technical writeup exists (3 pages or less)
- [ ] Code is accessible (GitHub repository)
- [ ] All components follow provided template
- [ ] Submission deadline: [CHECK DATE]

**VALIDATION COMMAND:**
```bash
# Check video file
ls -lh docs/challenge/demo_video.mp4
# Should be < 500MB, duration < 3:00

# Check writeup
wc -w docs/challenge/technical_writeup.pdf
# Should be ~1500-2500 words (3 pages)

# Check repository is public
git remote -v
# Verify GitHub URL is accessible
```

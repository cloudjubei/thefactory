# Agent Execution Checklist

This checklist ensures consistent, successful feature execution by any LLM agent.

## Pre-Execution Checklist

### ✅ Task Preparation
- [ ] Read `tasks/TASKS.md` to identify target task
- [ ] Read `tasks/{task_id}/plan_{task_id}.md` (create if missing)
- [ ] Identify next Pending (`-`) feature in plan
- [ ] Verify feature has complete Context field

### ✅ Context Gathering
- [ ] Use `read_plan_feature` to get feature details
- [ ] Use `retrieve_context_files` for ALL Context files listed
- [ ] Read ANY existing files that will be modified
- [ ] Check for related test files
- [ ] Use `ask_question` if any context is missing

## Feature Execution Checklist

### ✅ Implementation Phase
- [ ] Use `update_feature_status` to change from `-` to `~`
- [ ] Implement ONLY the current feature (not multiple features)
- [ ] Follow the feature's Action and Acceptance criteria exactly
- [ ] Make incremental changes to existing files (don't rewrite completely)

### ✅ Testing Phase
- [ ] Create test file: `tasks/{task_id}/tests/test_{task_id}_{feature_number}.py`
- [ ] Write tests that verify each Acceptance criterion
- [ ] Use `run_tests` tool to validate test passes
- [ ] Fix any failures before proceeding

### ✅ Completion Phase
- [ ] Use `update_feature_status` to change from `~` to `+`
- [ ] Use `finish_feature` with descriptive message
- [ ] Use `finish` to end execution cycle

## Error Prevention Rules

### 🚫 Never Do:
- Work on multiple features in one cycle
- Assume file contents without reading them
- Skip test creation
- Mark feature complete with failing tests
- Proceed with incomplete context

### ✅ Always Do:
- Read existing files before modifying
- Create tests immediately after implementation
- Ask questions when context is unclear
- Update feature status accurately
- Complete one feature fully before ending cycle

## Common Failure Points

### Issue: "Feature seems complete but tests fail"
**Solution**: Fix implementation or test, re-run until passing

### Issue: "Context files are missing or unclear"
**Solution**: Use `ask_question` to clarify requirements

### Issue: "Existing file content is different than expected"
**Solution**: Read current content, make incremental changes only

### Issue: "Multiple features seem related"
**Solution**: Focus on ONE feature only, handle dependencies in separate cycles
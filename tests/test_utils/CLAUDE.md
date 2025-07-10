# tests/test_utils/ Directory

This directory contains unit tests for utility functions and helper modules in the "Aim for the Stars" application.

## Test Files

### `test_goal_helpers.py` - Goal Utility Tests
- **Purpose**: Test goal-related utility functions and calculations
- **Coverage**: Goal progress calculations, status management, deadline handling

### `test_progress_helpers.py` - Progress Utility Tests
- **Purpose**: Test progress tracking and statistics utilities
- **Coverage**: Daily statistics, streak calculations, progress analytics

## Future Test Files

### `test_search_helpers.py` - Search Utility Tests (To Be Added)
- **Purpose**: Test search functionality and content processing utilities
- **Coverage**: Search algorithms, result ranking, snippet generation

## Utility Testing Categories

### Goal Helper Functions (`test_goal_helpers.py`)

#### Progress Calculation Testing
- **Goal completion percentage**: Accurate calculation of goal progress
- **Progress tracking**: Progress updates based on diary entries and activities
- **Target achievement**: Detection of goal target achievement
- **Progress history**: Historical progress tracking and trends

#### Status Management Testing
- **Status transitions**: Valid goal status changes (active/completed/paused)
- **Status validation**: Proper validation of status change requests
- **Automated status updates**: Automatic status changes based on conditions
- **Status history**: Tracking of goal status change history

#### Deadline and Date Handling
- **Deadline calculations**: Time remaining until goal target dates
- **Date validation**: Validation of goal target dates and ranges
- **Overdue detection**: Identification of overdue goals
- **Date formatting**: Proper date formatting for display and calculations

### Progress Helper Functions (`test_progress_helpers.py`)

#### Statistics Calculation Testing
- **Daily point totals**: Accurate calculation of daily points from entries
- **Weekly/monthly aggregation**: Aggregation of statistics over time periods
- **Average calculations**: Average points per day, week, month
- **Trend analysis**: Progress trend calculations and analysis

#### Streak Calculation Testing
- **Current streak calculation**: Accurate current streak counting
- **Longest streak tracking**: Proper tracking of longest achieved streaks
- **Streak reset logic**: Correct streak reset when continuity is broken
- **Streak types**: Different types of streaks (daily entries, positive behavior)

#### Data Visualization Helpers
- **Chart data formatting**: Preparation of data for Chart.js visualization
- **Date range filtering**: Filtering progress data by date ranges
- **Data aggregation**: Aggregating data for different chart types
- **Performance optimization**: Efficient data processing for large datasets

### Search Helper Functions (Future)

#### Search Algorithm Testing
- **Full-text search**: Comprehensive content search through diary entries
- **Relevance ranking**: Proper ranking of search results by relevance
- **Search performance**: Efficient search execution for large datasets
- **Search filtering**: Filtering search results by various criteria

#### Content Processing Testing
- **Snippet generation**: Creation of search result snippets with highlights
- **Content indexing**: Proper indexing of diary entry content
- **Search highlighting**: Highlighting of search terms in results
- **Content sanitization**: Proper sanitization of search content

## Testing Patterns

### Pure Function Testing
```python
def test_calculate_goal_progress():
    """Test goal progress calculation with various scenarios"""
    # Test with no progress
    progress = calculate_goal_progress(current=0, target=100)
    assert progress == 0.0
    
    # Test with partial progress
    progress = calculate_goal_progress(current=50, target=100)
    assert progress == 50.0
    
    # Test with completed goal
    progress = calculate_goal_progress(current=100, target=100)
    assert progress == 100.0
```

### Data Processing Testing
```python
def test_streak_calculation_with_gaps():
    """Test streak calculation with missing days"""
    entries = [
        {'date': '2023-01-01', 'rating': 1},
        {'date': '2023-01-02', 'rating': 1},
        # Gap on 2023-01-03
        {'date': '2023-01-04', 'rating': 1},
    ]
    
    streak = calculate_current_streak(entries)
    assert streak == 1  # Streak resets due to gap
```

### Edge Case Testing
```python
def test_progress_calculation_edge_cases():
    """Test progress calculation with edge cases"""
    # Test division by zero
    progress = calculate_progress(current=10, target=0)
    assert progress == 100.0  # Or handle as special case
    
    # Test negative values
    progress = calculate_progress(current=-5, target=10)
    assert progress == 0.0  # Negative progress should be 0
    
    # Test exceeding target
    progress = calculate_progress(current=150, target=100)
    assert progress == 100.0  # Cap at 100%
```

## Test Data Management

### Mock Data Creation
- **Realistic test data**: Test data that represents real user scenarios
- **Edge case data**: Data that tests boundary conditions and edge cases
- **Large dataset simulation**: Testing with large amounts of data
- **Varied scenarios**: Different combinations of input data

### Data Factory Patterns
- **Goal factory**: Generate test goals with various properties
- **Entry factory**: Create test diary entries with different characteristics
- **Statistics factory**: Generate test statistics data for various scenarios
- **Date range factory**: Create test date ranges for time-based testing

### Performance Test Data
- **Scalability testing**: Large datasets to test performance limits
- **Memory usage**: Data that tests memory efficiency
- **Processing speed**: Time-sensitive operations with large datasets
- **Optimization validation**: Data that validates optimization improvements

## Integration Testing

### Database Integration
- **Query efficiency**: Utility functions execute efficient database queries
- **Transaction handling**: Proper database transaction management
- **Data consistency**: Utilities maintain data consistency across operations
- **Error handling**: Graceful handling of database errors

### Model Integration
- **Model interaction**: Utilities work correctly with SQLAlchemy models
- **Relationship handling**: Proper handling of model relationships
- **Validation integration**: Utilities respect model validation rules
- **Business logic**: Utilities implement correct business logic

### Flask Integration
- **Request context**: Utilities work within Flask request context
- **Session handling**: Utilities respect user sessions and authentication
- **Configuration access**: Utilities access application configuration correctly
- **Error propagation**: Proper error handling and propagation to routes

## Performance Testing

### Algorithm Efficiency
- **Time complexity**: Utilities execute within acceptable time limits
- **Space complexity**: Efficient memory usage for all operations
- **Scalability**: Performance remains acceptable with increasing data size
- **Optimization**: Continuous optimization of critical utility functions

### Caching Testing
- **Cache effectiveness**: Caching improves performance as expected
- **Cache invalidation**: Cache invalidation works correctly
- **Memory management**: Cached data doesn't cause memory leaks
- **Cache consistency**: Cached data remains consistent with source data

### Benchmark Testing
- **Performance baselines**: Establish performance baselines for utilities
- **Regression testing**: Detect performance regressions in utility functions
- **Optimization verification**: Verify performance improvements from optimizations
- **Comparative analysis**: Compare different algorithm implementations

## Development Workflow

### Adding Utility Tests
1. **Create utility**: Implement new utility function with clear purpose
2. **Write tests**: Create comprehensive tests covering all scenarios
3. **Test edge cases**: Ensure proper handling of edge cases and errors
4. **Performance test**: Verify utility performance with realistic data sizes
5. **Integration test**: Test utility integration with other components

### Utility Test Maintenance
- **Regular review**: Periodically review utility function efficiency
- **Performance monitoring**: Monitor utility performance in production
- **Refactoring**: Refactor utilities for better performance and maintainability
- **Documentation**: Keep utility documentation current and comprehensive

### Debugging Utility Issues
1. **Isolate problem**: Create minimal test that reproduces the issue
2. **Check inputs**: Verify utility receives expected input data
3. **Review algorithm**: Check algorithm logic and implementation
4. **Test edge cases**: Ensure edge cases are handled correctly
5. **Fix and optimize**: Implement fix and optimize if necessary
from datetime import datetime
import base64
from io import BytesIO
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from flask import render_template, current_app
import matplotlib.pyplot as plt
import os

def generate_journey_pdf(user, entries, points_data, weekday_data, top_days, stats, wordcloud_image=None, goal_stats=None, goal_history=None):
    """Generate a PDF containing the user's self-reflective journey.
    
    Args:
        user: User model instance
        entries: List of diary entries
        points_data: List of [date, points] for the points graph
        weekday_data: List of weekday performance data
        top_days: List of top performing days with entries
        stats: Dictionary containing user statistics
        wordcloud_image: Optional base64 data URL of the word cloud image
        goal_stats: Dictionary containing goal statistics
        goal_history: List of completed/failed goals
    
    Returns:
        BytesIO object containing the generated PDF
    """
    # Debug logging
    print(f"PDF Generator received {len(entries)} entries")
    print("First few entries:")
    for entry in entries[:3]:
        print(f"- {entry.entry_date}: {entry.content[:50]}...")

    # Create a BytesIO buffer for the PDF
    pdf_buffer = BytesIO()
    
    # Generate static images of the charts
    points_chart = _generate_points_chart(points_data)
    weekday_chart = _generate_weekday_chart(weekday_data)
    
    # Generate goal category chart if goal stats are available
    goal_chart = None
    if goal_stats and goal_stats.get('has_stats'):
        goal_chart = _generate_goal_category_chart(goal_stats['category_stats'])
    
    # Prepare wordcloud image (strip data URL prefix if present)
    wordcloud_chart = None
    if wordcloud_image and wordcloud_image.startswith('data:image/png;base64,'):
        wordcloud_chart = wordcloud_image.split(',', 1)[1]
    elif wordcloud_image:
        wordcloud_chart = wordcloud_image

    # Sort entries chronologically (earliest first)
    sorted_entries = sorted(entries, key=lambda x: x.entry_date)
    print(f"Sorted {len(sorted_entries)} entries for PDF")
    
    # Prepare the HTML content
    html_content = render_template(
        'pdf/journey.html',
        user=user,
        entries=sorted_entries,  # Pass the sorted entries
        points_chart=points_chart,
        weekday_chart=weekday_chart,
        goal_chart=goal_chart,
        wordcloud_chart=wordcloud_chart,
        top_days=top_days,
        stats=stats,
        goal_stats=goal_stats,
        goal_history=goal_history,
        generation_date=datetime.now().strftime('%B %d, %Y')
    )
    
    # Log HTML content length for debugging
    print(f"Generated HTML content length: {len(html_content)}")
    
    # Configure fonts
    font_config = FontConfiguration()
    
    # Load external CSS file
    css_file_path = os.path.join(current_app.static_folder, 'css', 'pdf_journey.css')
    
    # Define page-specific CSS for PDF styling
    page_css = CSS(string='''
        @page {
            margin: 1cm;
            size: letter;
            @bottom-right {
                content: "Page " counter(page);
            }
            @bottom-left {
                content: "Generated from aimforthestars.com";
                font-size: 9pt;
                color: #666;
            }
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.4;
            color: #000;
        }
        .watermark {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-45deg);
            font-size: 72pt;
            opacity: 0.1;
            z-index: -1;
        }
    ''', font_config=font_config)
    
    # Load external CSS file
    external_css = CSS(filename=css_file_path, font_config=font_config)
    
    # Generate PDF with both CSS files
    HTML(string=html_content).write_pdf(
        pdf_buffer,
        stylesheets=[external_css, page_css],
        font_config=font_config
    )
    
    # Reset buffer position
    pdf_buffer.seek(0)
    return pdf_buffer

def _generate_points_chart(points_data):
    """Generate a static image of the points over time chart."""
    plt.figure(figsize=(10, 6))
    plt.style.use('dark_background')
    
    # Extract dates and points
    dates = [item[0] for item in points_data]
    points = [item[1] for item in points_data]
    
    # Create the line plot
    plt.plot(dates, points, color='teal', linewidth=2)
    
    # Customize the plot
    plt.title('Points Over Time', pad=20)
    plt.xlabel('Date')
    plt.ylabel('Total Points')
    plt.grid(True, alpha=0.2)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(image_png).decode()

def _generate_weekday_chart(weekday_data):
    """Generate a static image of the weekday performance chart."""
    plt.figure(figsize=(10, 6))
    plt.style.use('dark_background')
    
    # Extract data
    days = [day['name'] for day in weekday_data]
    avg_points = [day['avg_points'] for day in weekday_data]
    
    # Create the bar plot
    bars = plt.bar(days, avg_points, color='teal')
    
    # Customize the plot
    plt.title('Average Points by Day of Week', pad=20)
    plt.ylabel('Average Points')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom')
    
    # Adjust layout
    plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(image_png).decode()

def _generate_goal_category_chart(category_stats):
    """Generate a static image of the goal category performance chart."""
    plt.figure(figsize=(12, 8))
    plt.style.use('dark_background')
    
    # Extract data
    categories = list(category_stats.keys())
    completed_data = [category_stats[cat]['completed'] for cat in categories]
    failed_data = [category_stats[cat]['failed'] for cat in categories]
    
    # Filter out categories with no goals
    non_zero_categories = []
    non_zero_completed = []
    non_zero_failed = []
    
    for i, cat in enumerate(categories):
        if completed_data[i] > 0 or failed_data[i] > 0:
            non_zero_categories.append(cat)
            non_zero_completed.append(completed_data[i])
            non_zero_failed.append(failed_data[i])
    
    if not non_zero_categories:
        # If no goals, create a simple text plot
        plt.figure(figsize=(8, 4))
        plt.text(0.5, 0.5, 'No completed or failed goals yet', 
                ha='center', va='center', transform=plt.gca().transAxes,
                fontsize=14, color='white')
        plt.axis('off')
    else:
        # Create the stacked bar chart
        x = range(len(non_zero_categories))
        width = 0.6
        
        # Create bars
        completed_bars = plt.bar(x, non_zero_completed, width, 
                               label='Completed', color='#00ff7f', alpha=0.8)
        failed_bars = plt.bar(x, non_zero_failed, width, 
                            bottom=non_zero_completed, label='Failed', 
                            color='#ff6384', alpha=0.8)
        
        # Customize the plot
        plt.title('Goal Performance by Category', pad=20, fontsize=16)
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Number of Goals', fontsize=12)
        plt.xticks(x, non_zero_categories, rotation=45, ha='right')
        plt.legend()
        plt.grid(True, alpha=0.2, axis='y')
        
        # Add value labels on bars
        for i, (comp, fail) in enumerate(zip(non_zero_completed, non_zero_failed)):
            if comp > 0:
                plt.text(i, comp/2, str(comp), ha='center', va='center', 
                        fontweight='bold', color='black')
            if fail > 0:
                plt.text(i, comp + fail/2, str(fail), ha='center', va='center', 
                        fontweight='bold', color='black')
    
    # Adjust layout
    plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight', 
                facecolor='#1a1a2e', edgecolor='none')
    plt.close()
    
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(image_png).decode() 
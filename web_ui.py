import streamlit as st
import json
from datetime import datetime, timedelta
import random
from facebook_rental_agent import FacebookRentalAgent

# Page configuration
st.set_page_config(
    page_title="Facebook Rental Agent - Isla Vista",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .post-preview {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .stats-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .theme-badge {
        background-color: #1f77b4;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 0.2rem;
    }
    .campus-badge {
        background-color: #ff7f0e;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🏠 Facebook Rental Agent</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666;">Isla Vista Apartment Marketing</h3>', unsafe_allow_html=True)
    
    # Initialize agent
    try:
        agent = FacebookRentalAgent()
        st.success("✅ Agent initialized successfully!")
    except Exception as e:
        st.error(f"❌ Error initializing agent: {e}")
        return
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # Campus preference
        st.subheader("🎯 Target Campus")
        campus_preference = st.selectbox(
            "Select primary target:",
            ["UCSB (70%) + SBCC (30%)", "UCSB Only", "SBCC Only", "Random"]
        )
        
        # Theme selection
        st.subheader("📌 Post Theme")
        theme_options = ["Random"] + [theme.replace('_', ' ').title() for theme in agent.post_themes]
        selected_theme = st.selectbox("Choose theme:", theme_options)
        
        # Number of posts
        st.subheader("📊 Generation")
        num_posts = st.slider("Number of posts to generate:", 1, 10, 3)
        
        # Generate button
        if st.button("🚀 Generate Posts", type="primary"):
            st.session_state.generate_posts = True
            st.session_state.campus_pref = campus_preference
            st.session_state.selected_theme = selected_theme
            st.session_state.num_posts = num_posts
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📱 Generated Posts")
        
        # Move the generation logic here so posts appear in the left column
        if 'generate_posts' in st.session_state and st.session_state.generate_posts:
            with st.spinner("Generating posts..."):
                posts = []
                
                for i in range(st.session_state.num_posts):
                    # Override campus selection if specified
                    if st.session_state.campus_pref == "UCSB Only":
                        # Force UCSB by temporarily modifying the agent
                        original_weights = agent.generate_daily_post.__defaults__
                        agent.generate_daily_post.__defaults__ = (["UCSB"],)
                    elif st.session_state.campus_pref == "SBCC Only":
                        agent.generate_daily_post.__defaults__ = (["SBCC"],)
                    
                    post = agent.generate_daily_post()
                    
                    # Override theme if specified
                    if st.session_state.selected_theme != "Random":
                        theme_name = st.session_state.selected_theme.lower().replace(' ', '_')
                        post['theme'] = theme_name
                    
                    posts.append(post)
                
                st.session_state.generated_posts = posts
                st.session_state.generate_posts = False
        
        # Display generated posts in the left column
        if 'generated_posts' in st.session_state:
            for i, post in enumerate(st.session_state.generated_posts):
                with st.expander(f"📝 Post {i+1} - {post['theme'].replace('_', ' ').title()}", expanded=True):
                    col_post, col_meta = st.columns([3, 1])
                    
                    with col_post:
                        st.markdown("### 📱 Facebook Preview")
                        st.markdown(f"""
                        <div class="post-preview">
                            <strong>🏠 Your Name • {post['date']}</strong><br><br>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display post content with preserved line breaks
                        post_content_formatted = post['content'].replace('\n', '<br>')
                        st.markdown(f"""
                        <div class="post-preview">
                            {post_content_formatted}<br><br>
                            <em>👍 Like • 💬 Comment • 🔄 Share</em>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_meta:
                        st.markdown("### 📊 Post Details")
                        st.markdown(f"""
                        <div class="stats-card">
                            <span class="campus-badge">{post['target_campus']}</span><br>
                            <span class="theme-badge">{post['theme'].replace('_', ' ').title()}</span><br><br>
                            <strong>Style:</strong> {post['creative_style'].replace('_', ' ').title()}<br>
                            <strong>Model:</strong> {post['model_used']}<br>
                            <strong>Characters:</strong> {post['character_count']}<br>
                            <strong>Generated:</strong> {datetime.now().strftime('%H:%M:%S')}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Action buttons
                    col_actions = st.columns(3)
                    with col_actions[0]:
                        if st.button(f"💾 Save Post {i+1}", key=f"save_{i}"):
                            filename = f"post_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                            with open(filename, 'w') as f:
                                json.dump(post, f, indent=2)
                            st.success(f"✅ Saved as {filename}")
                    
                    with col_actions[1]:
                        if st.button(f"🔄 Regenerate {i+1}", key=f"regen_{i}"):
                            st.session_state.regenerate_post = i
                            st.rerun()
                    
                    with col_actions[2]:
                        if st.button(f"📋 Copy Text {i+1}", key=f"copy_{i}"):
                            st.code(post['full_post'])
    
    with col2:
        st.header("📈 Statistics")
        
        # Agent stats
        st.markdown("### 🤖 Agent Info")
        st.markdown(f"""
        <div class="stats-card">
            <strong>Model:</strong> {agent.model_name}<br>
            <strong>Themes:</strong> {len(agent.post_themes)}<br>
            <strong>Templates:</strong> {sum(len(templates) for templates in agent.post_templates.values())}<br>
            <strong>Style:</strong> Clean (No emojis/hashtags)
        </div>
        """, unsafe_allow_html=True)
        
        # Theme breakdown
        st.markdown("### 🎨 Available Themes")
        for theme in agent.post_themes:
            theme_name = theme.replace('_', ' ').title()
            st.markdown(f"• {theme_name}")
        
        # Campus targeting info
        st.markdown("### 🎯 Campus Targeting")
        st.markdown("""
        <div class="stats-card">
            <strong>UCSB:</strong> 70% priority<br>
            <strong>SBCC:</strong> 30% secondary<br>
            <strong>Focus:</strong> Walkability & convenience
        </div>
        """, unsafe_allow_html=True)
        
        # Quick actions
        st.header("⚡ Quick Actions")
        
        if st.button("🎲 Random Post"):
            post = agent.generate_daily_post()
            st.session_state.quick_post = post
            st.rerun()
        
        if st.button("📅 Weekly Preview"):
            weekly_posts = agent.schedule_weekly_posts()
            st.session_state.weekly_posts = weekly_posts
            st.rerun()
        
        if st.button("📊 Theme Analysis"):
            st.session_state.show_analysis = True
            st.rerun()
    
    # Quick post display
    if 'quick_post' in st.session_state:
        st.markdown("### 🎲 Random Post")
        post = st.session_state.quick_post
        st.markdown(f"""
        <div class="post-preview">
            <strong>🏠 Your Name • {post['date']}</strong><br><br>
            {post['content']}<br><br>
            {post['hashtags']}
        </div>
        """, unsafe_allow_html=True)
        del st.session_state.quick_post
    
    # Weekly posts display
    if 'weekly_posts' in st.session_state:
        st.markdown("### 📅 Weekly Posts Preview")
        for i, post in enumerate(st.session_state.weekly_posts):
            st.markdown(f"**Day {i+1} ({post['date']}):** {post['theme'].replace('_', ' ').title()} - {post['target_campus']}")
        del st.session_state.weekly_posts
    
    # Theme analysis
    if 'show_analysis' in st.session_state:
        st.markdown("### 📊 Theme Analysis")
        
        # Generate sample posts for each theme
        theme_samples = {}
        for theme in agent.post_themes:
            theme_samples[theme] = []
            for _ in range(3):
                post = agent.generate_daily_post()
                if post['theme'] == theme:
                    theme_samples[theme].append(post)
        
        # Display analysis
        for theme, posts in theme_samples.items():
            with st.expander(f"📌 {theme.replace('_', ' ').title()} ({len(posts)} samples)"):
                for j, post in enumerate(posts):
                    st.markdown(f"**Sample {j+1}:** {post['target_campus']} - {post['creative_style'].replace('_', ' ').title()}")
                    st.text(post['content'][:100] + "...")
        
        del st.session_state.show_analysis

if __name__ == "__main__":
    main() 
#!/usr/bin/env python
from dotenv import load_dotenv
from .flow import GuideGeneratorFlow
from .utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger("main")


def get_inputs():
    """Interactive terminal interface to collect user inputs"""
    print("\n" + "=" * 70)
    print("🎯 GUIDE GENERATOR - INPUT COLLECTION")
    print("=" * 70)
    print("\nWelcome! Let's create a getting-started guide for your framework/tool.")
    print("\nℹ️  All source inputs are OPTIONAL. You can skip any by pressing Enter.")
    print("=" * 70)
    
    # YouTube Links
    print("\n" + "─" * 70)
    print("\n📺 YOUTUBE VIDEOS/CHANNELS")
    print("   You can provide:")
    print("   - Individual video URLs (e.g., https://youtube.com/watch?v=abc123)")
    print("   - Channel URLs (e.g., https://youtube.com/@channelname)")
    print("   - Multiple links separated by commas")
    youtube_links = input("\n   Enter YouTube links (or press Enter to skip): ").strip()
    
    # Web Page Links
    print("\n" + "─" * 70)
    print("\n🌐 WEB PAGES/ARTICLES")
    print("   You can provide:")
    print("   - Documentation URLs")
    print("   - Blog posts or tutorials")
    print("   - Multiple links separated by commas")
    webpage_links = input("\n   Enter web page URLs (or press Enter to skip): ").strip()
    
    # Research Papers
    print("\n" + "─" * 70)
    print("\n📄 RESEARCH PAPERS (arXiv)")
    print("   You can provide:")
    print("   - arXiv URLs (e.g., https://arxiv.org/abs/2103.xxxxx)")
    print("   - Paper titles or arXiv IDs")
    print("   - Multiple entries separated by commas")
    research_paper_links = input("\n   Enter research paper links/queries (or press Enter to skip): ").strip()
    
    # Documents
    print("\n" + "─" * 70)
    print("\n📁 DOCUMENTS (PDF/Text/Markdown)")
    print("   You can provide:")
    print("   - Local file paths to PDFs")
    print("   - Text file paths (.txt)")
    print("   - Markdown file paths (.md, .mdx)")
    print("   - Multiple paths separated by commas")
    document_paths = input("\n   Enter document paths (or press Enter to skip): ").strip()
    
    return {
        'youtube_links': youtube_links,
        'webpage_links': webpage_links,
        'research_paper_links': research_paper_links,
        'document_paths': document_paths
    }


def run():
    """Main execution function"""
    try:
        # Get inputs
        inputs = get_inputs()
        
        # Initialize flow
        flow = GuideGeneratorFlow()
        
        # Run flow
        logger.info("Starting guide generation flow...")
        result = flow.kickoff(inputs=inputs)
        
        print("\n" + "=" * 70)
        print("✅ GENERATION COMPLETE")
        print("=" * 70)
        print(f"Status: {result}")
        print("\nCheck 'outputs' folder for your guide!")
        print("=" * 70)
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Process interrupted by user")
        print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    run()
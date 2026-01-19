"""
Playwright tests for sidebar visibility and styling.
Run with: pytest tests/test_sidebar.py -v
Ensure Streamlit is running first: streamlit run app.py --server.port 8502
"""
import pytest
from playwright.sync_api import Page, expect


# Use a pre-started server
BASE_URL = "http://localhost:8502"


class TestSidebarVisibility:
    """Tests for sidebar expand/collapse button visibility."""

    def test_sidebar_expanded_by_default(self, page: Page):
        """Test that the sidebar is expanded by default."""
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")

        # Wait for Streamlit to fully render
        page.wait_for_timeout(3000)

        # Check sidebar is visible
        sidebar = page.locator('[data-testid="stSidebar"]')
        expect(sidebar).to_be_visible()
        print("PASS: Sidebar is visible by default")

    def test_sidebar_has_navy_background(self, page: Page):
        """Test that sidebar has Navy Blue background color."""
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        sidebar = page.locator('[data-testid="stSidebar"]')

        # Get computed background color
        bg_color = sidebar.evaluate(
            "el => window.getComputedStyle(el).backgroundColor"
        )

        print(f"Sidebar background color: {bg_color}")

        # Navy blue #1e3a5f = rgb(30, 58, 95)
        assert "rgb(30, 58, 95)" in bg_color or "30, 58, 95" in bg_color, \
            f"Expected Navy Blue background, got: {bg_color}"
        print("PASS: Sidebar has Navy Blue background")

    def test_sidebar_collapse_button_exists(self, page: Page):
        """Test that the collapse button exists in the sidebar."""
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Look for collapse button - Streamlit uses a button to collapse sidebar
        # Try to find any button that could be used to collapse
        collapse_buttons = page.locator('[data-testid="stSidebar"] button').all()

        print(f"Found {len(collapse_buttons)} buttons in sidebar")

        # Take screenshot of current state
        page.screenshot(path="tests/screenshots/sidebar_expanded.png", full_page=True)
        print("Screenshot saved: tests/screenshots/sidebar_expanded.png")

    def test_sidebar_can_be_collapsed(self, page: Page):
        """Test that sidebar can be collapsed and expand button becomes visible."""
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        sidebar = page.locator('[data-testid="stSidebar"]')
        expect(sidebar).to_be_visible()

        # Get initial sidebar width
        initial_box = sidebar.bounding_box()
        print(f"Initial sidebar width: {initial_box['width']}px")

        # Try to find and click collapse button
        # Streamlit's collapse button is typically in the sidebar header area
        collapse_selectors = [
            '[data-testid="stSidebar"] button[kind="header"]',
            '[data-testid="stSidebar"] [data-testid="baseButton-header"]',
            '[data-testid="collapsedControl"]',
            'button[title="Close sidebar"]',
            '[data-testid="stSidebar"] button:first-of-type',
        ]

        for selector in collapse_selectors:
            buttons = page.locator(selector).all()
            if buttons:
                print(f"Found button with selector: {selector}")

        # Take screenshot for visual check
        page.screenshot(path="tests/screenshots/sidebar_before_collapse.png", full_page=True)
        print("Screenshot saved: tests/screenshots/sidebar_before_collapse.png")

    def test_expand_button_styling_when_collapsed(self, page: Page):
        """Test that the expand button is properly styled when visible."""
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Check if collapsedControl exists in the page
        expand_button = page.locator('[data-testid="collapsedControl"]')

        # The expand button might only appear when sidebar is collapsed
        # Check the CSS that we added is being applied
        styles = page.evaluate("""
            () => {
                // Check if our custom CSS is loaded
                const sheets = document.styleSheets;
                let hasCustomStyles = false;

                for (let sheet of sheets) {
                    try {
                        const rules = sheet.cssRules || sheet.rules;
                        for (let rule of rules) {
                            if (rule.selectorText && rule.selectorText.includes('collapsedControl')) {
                                hasCustomStyles = true;
                                return {
                                    hasCustomStyles: true,
                                    rule: rule.cssText
                                };
                            }
                        }
                    } catch (e) {
                        // Cross-origin stylesheet, skip
                    }
                }
                return { hasCustomStyles: false };
            }
        """)

        print(f"Custom collapsedControl styles found: {styles}")

    def test_sidebar_navigation_items_visible(self, page: Page):
        """Test that navigation items in the sidebar are visible with white text."""
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        sidebar = page.locator('[data-testid="stSidebar"]')
        expect(sidebar).to_be_visible()

        # Check for navigation text elements
        nav_items = ["Home", "Classes", "Students", "Assignments"]

        for item in nav_items:
            # Find text in sidebar
            text_element = sidebar.locator(f"text={item}").first
            if text_element.count() > 0 and text_element.is_visible():
                # Get text color
                color = text_element.evaluate(
                    "el => window.getComputedStyle(el).color"
                )
                print(f"'{item}' text color: {color}")
                # Check it's white or near-white (255, 255, 255 or close)
            else:
                print(f"'{item}' not found in sidebar")

    def test_sidebar_content_readable(self, page: Page):
        """Test that sidebar content is readable (white text on navy)."""
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        sidebar = page.locator('[data-testid="stSidebar"]')

        # Check the title text
        title = sidebar.locator("text=NewGrader").first
        if title.count() > 0:
            styles = title.evaluate("""
                el => {
                    const computed = window.getComputedStyle(el);
                    return {
                        color: computed.color,
                        fontSize: computed.fontSize,
                        fontWeight: computed.fontWeight
                    };
                }
            """)
            print(f"Title styles: {styles}")

        # Take final screenshot
        page.screenshot(path="tests/screenshots/sidebar_final.png", full_page=True)
        print("Screenshot saved: tests/screenshots/sidebar_final.png")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

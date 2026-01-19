"""
Debug test for sidebar functionality - comprehensive testing
"""
import pytest
from playwright.sync_api import Page, expect
import time

BASE_URL = "http://localhost:8502"

def test_sidebar_comprehensive_debug(page: Page):
    """Comprehensive test to debug sidebar behavior."""

    print("\n" + "="*60)
    print("STARTING COMPREHENSIVE SIDEBAR DEBUG TEST")
    print("="*60)

    # 1. Navigate to the page
    print("\n1. Navigating to application...")
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")

    # Wait for Streamlit to fully initialize
    print("   Waiting for Streamlit to initialize...")
    page.wait_for_timeout(3000)

    # 2. Check initial sidebar state
    print("\n2. Checking initial sidebar state...")
    sidebar = page.locator('[data-testid="stSidebar"]')

    # Check if sidebar exists
    if sidebar.count() > 0:
        print("   [OK] Sidebar element found")

        # Check visibility
        is_visible = sidebar.is_visible()
        print(f"   Sidebar visible: {is_visible}")

        # Get aria-expanded attribute
        aria_expanded = sidebar.get_attribute('aria-expanded')
        print(f"   Sidebar aria-expanded: {aria_expanded}")

        # Get computed styles
        sidebar_styles = sidebar.evaluate("""
            el => {
                const computed = window.getComputedStyle(el);
                const rect = el.getBoundingClientRect();
                return {
                    display: computed.display,
                    visibility: computed.visibility,
                    transform: computed.transform,
                    width: computed.width,
                    position: computed.position,
                    left: computed.left,
                    backgroundColor: computed.backgroundColor,
                    zIndex: computed.zIndex,
                    boundingRect: {
                        left: rect.left,
                        width: rect.width,
                        visible: rect.width > 0 && rect.height > 0
                    }
                };
            }
        """)

        print("   Sidebar computed styles:")
        for key, value in sidebar_styles.items():
            if key == 'boundingRect':
                print(f"     - Bounding rect:")
                for k, v in value.items():
                    print(f"       - {k}: {v}")
            else:
                print(f"     - {key}: {value}")

        # Take screenshot
        page.screenshot(path="tests/screenshots/debug_1_initial_state.png", full_page=True)
        print("   Screenshot saved: debug_1_initial_state.png")

    else:
        print("   [ERROR] Sidebar element NOT found!")
        page.screenshot(path="tests/screenshots/debug_1_no_sidebar.png", full_page=True)

    # 3. Check for collapse/expand button
    print("\n3. Checking for collapse/expand controls...")

    # Check for collapsed control (expand button)
    collapsed_control = page.locator('[data-testid="collapsedControl"]')
    if collapsed_control.count() > 0:
        is_visible = collapsed_control.is_visible()
        print(f"   Collapsed control found, visible: {is_visible}")

        if is_visible:
            control_styles = collapsed_control.evaluate("""
                el => {
                    const computed = window.getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    return {
                        display: computed.display,
                        visibility: computed.visibility,
                        width: computed.width,
                        height: computed.height,
                        backgroundColor: computed.backgroundColor,
                        position: {
                            left: rect.left,
                            top: rect.top
                        }
                    };
                }
            """)
            print("   Collapsed control styles:")
            for key, value in control_styles.items():
                print(f"     - {key}: {value}")
    else:
        print("   No collapsed control found")

    # Check for sidebar buttons (collapse button)
    sidebar_buttons = page.locator('[data-testid="stSidebar"] button').all()
    print(f"   Found {len(sidebar_buttons)} buttons in sidebar")

    for i, button in enumerate(sidebar_buttons):
        try:
            button_info = button.evaluate("""
                el => {
                    return {
                        text: el.textContent,
                        title: el.title,
                        ariaLabel: el.getAttribute('aria-label'),
                        kind: el.getAttribute('kind'),
                        visible: el.offsetParent !== null
                    };
                }
            """)
            print(f"   Button {i}: {button_info}")
        except:
            print(f"   Button {i}: Could not get info")

    # 4. Try to collapse the sidebar
    print("\n4. Attempting to collapse sidebar...")

    # Try different methods to find collapse button
    collapse_selectors = [
        '[data-testid="stSidebar"] button[kind="header"]',
        '[data-testid="stSidebar"] button[kind="headerNoPadding"]',
        '[data-testid="stSidebar"] [data-testid="baseButton-header"]',
        '[data-testid="stSidebar"] [data-testid="baseButton-headerNoPadding"]',
        '[data-testid="stSidebar"] button:has(svg)',
        'button[title*="Close"]',
        'button[aria-label*="Close"]'
    ]

    collapse_button = None
    for selector in collapse_selectors:
        buttons = page.locator(selector).all()
        if buttons:
            print(f"   Found button with selector: {selector}")
            collapse_button = buttons[0]
            break

    if collapse_button:
        print("   Clicking collapse button...")
        page.screenshot(path="tests/screenshots/debug_2_before_collapse.png", full_page=True)

        try:
            collapse_button.click()
            print("   [OK] Clicked collapse button")

            # Wait for animation
            page.wait_for_timeout(1000)

            # Check sidebar state after collapse
            sidebar_after = page.locator('[data-testid="stSidebar"]')
            aria_after = sidebar_after.get_attribute('aria-expanded')
            is_visible_after = sidebar_after.is_visible()

            print(f"   After collapse - aria-expanded: {aria_after}")
            print(f"   After collapse - visible: {is_visible_after}")

            # Get position after collapse
            position_after = sidebar_after.evaluate("""
                el => {
                    const rect = el.getBoundingClientRect();
                    const computed = window.getComputedStyle(el);
                    return {
                        left: rect.left,
                        width: rect.width,
                        transform: computed.transform,
                        display: computed.display
                    };
                }
            """)
            print(f"   After collapse - position: {position_after}")

            page.screenshot(path="tests/screenshots/debug_3_after_collapse.png", full_page=True)

            # 5. Check if expand button appears
            print("\n5. Checking for expand button after collapse...")
            page.wait_for_timeout(500)

            expand_button = page.locator('[data-testid="collapsedControl"]')
            if expand_button.count() > 0 and expand_button.is_visible():
                print("   [OK] Expand button is visible")

                # Try to expand again
                print("   Clicking expand button...")
                expand_button.click()
                page.wait_for_timeout(1000)

                # Check final state
                final_expanded = sidebar_after.get_attribute('aria-expanded')
                final_visible = sidebar_after.is_visible()
                print(f"   After expand - aria-expanded: {final_expanded}")
                print(f"   After expand - visible: {final_visible}")

                page.screenshot(path="tests/screenshots/debug_4_after_expand.png", full_page=True)
            else:
                print("   [ERROR] Expand button not visible")

        except Exception as e:
            print(f"   [ERROR] Error clicking collapse button: {e}")
    else:
        print("   [ERROR] No collapse button found")

    # 6. Check our custom JavaScript
    print("\n6. Checking custom JavaScript...")

    js_check = page.evaluate("""
        () => {
            // Check if our custom function exists
            const hasEnsureFunction = typeof ensureSidebarVisible !== 'undefined';

            // Check for custom styles
            const sheets = document.styleSheets;
            let hasCustomStyles = false;
            let customRules = [];

            for (let sheet of sheets) {
                try {
                    const rules = sheet.cssRules || sheet.rules;
                    for (let rule of rules) {
                        if (rule.selectorText &&
                            (rule.selectorText.includes('stSidebar') ||
                             rule.selectorText.includes('collapsedControl'))) {
                            hasCustomStyles = true;
                            customRules.push(rule.selectorText);
                        }
                    }
                } catch (e) {
                    // Cross-origin stylesheet
                }
            }

            return {
                hasEnsureFunction: hasEnsureFunction,
                hasCustomStyles: hasCustomStyles,
                customRuleCount: customRules.length,
                sampleRules: customRules.slice(0, 5)
            };
        }
    """)

    print(f"   Custom JS function exists: {js_check.get('hasEnsureFunction', False)}")
    print(f"   Custom styles applied: {js_check.get('hasCustomStyles', False)}")
    print(f"   Custom rule count: {js_check.get('customRuleCount', 0)}")
    print(f"   Sample rules: {js_check.get('sampleRules', [])}")

    # 7. Final state check
    print("\n7. Final state summary:")
    final_sidebar = page.locator('[data-testid="stSidebar"]')
    if final_sidebar.count() > 0:
        final_state = final_sidebar.evaluate("""
            el => {
                const rect = el.getBoundingClientRect();
                return {
                    visible: el.offsetParent !== null,
                    ariaExpanded: el.getAttribute('aria-expanded'),
                    position: `${rect.left}px from left, ${rect.width}px wide`,
                    actuallyVisible: rect.width > 0 && rect.left > -rect.width
                };
            }
        """)

        for key, value in final_state.items():
            print(f"   - {key}: {value}")

    page.screenshot(path="tests/screenshots/debug_5_final_state.png", full_page=True)

    print("\n" + "="*60)
    print("SIDEBAR DEBUG TEST COMPLETE")
    print("Check screenshots in tests/screenshots/debug_*.png")
    print("="*60)

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
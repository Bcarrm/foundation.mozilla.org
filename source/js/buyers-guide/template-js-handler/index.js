import mobileNavStickinessHandler from "./mobile-nav-stickiness-handler";
import mobileSearchBar from "./mobile-search-bar";
import diveDeeperListExpansionHandler from "./product-page-dive-deeper-list";
import categoryDropdown from "./pni-category-dropdown";
import productCommentGaEventHandler from "./product-page-comment-handler";

/**
 * Bind event handlers
 */
export const bindEventHandlers = () => {
  mobileNavStickinessHandler();
  mobileSearchBar();
  diveDeeperListExpansionHandler();
  categoryDropdown();
  productCommentGaEventHandler();
};

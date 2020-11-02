### Type of Changes

- [ ] Small bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds new functionality)
- [ ] Breaking change (fix or feature that would change existing functionality)
- [ ] Deploy to staging (Merge from `dev` to `staging`)
- [ ] Release stable version (Merge from `staging` to `master`)

### Description

Removing sales in quota from xplor score formula

### Motivation and context

The `sale` property in bimbo data is rounding by quota, so was necessary parse it to pieces.

### Tests

* Run tests with `make run-tests`
* Open the view where the sales are shown
* Add screenshot:

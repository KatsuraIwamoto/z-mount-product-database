# Scope and principles

Z Mount Product Database maintains separate datasets for lenses and related optical products and for mount adapters.
This page explains what is in scope and how inclusion decisions are made.

!!! info "Cameras are outside the current scope"
    If camera data is added in the future, it will use a separate dataset.

## Confirming inclusion {#inclusion-criteria}

Include a candidate only after an official product release announcement or confirmed sale or availability.
Use the official product release-announcement date for `lifecycle.announcementDate`, never a development-announcement date.
If only a development announcement is available, the candidate remains a `needs-review` research result until a product release announcement or sale can be confirmed.

Inclusion means that a product release announcement or sale was confirmed in the past.
It does not mean that the product is currently sold, in stock, or available.

Absence from the distribution data does not mean that a product has not been investigated.
Each research result records whether the candidate product is included, excluded, or still needs review.

## Lenses and related optical products {#lens-dataset}

One dataset contains photographic lenses, cinema lenses, teleconverters, pinholes, and similar products sold for the Nikon Z mount.
The same verification standards apply to every manufacturer and brand.

### Included {#lens-included}

- Photographic lenses
- Cinema lenses
- Teleconverters
- Pinholes

Include products offered by the manufacturer for direct attachment to the Nikon Z mount, including products that use the manufacturer's own interchangeable rear mount.
Products that attach through an adapter qualify only when the manufacturer officially offers the Nikon Z configuration in one of these forms:

- The Z-mount adapter is supplied with the product
- The product uses a Z-mount adapter dedicated to that lens or product series

### Excluded {#lens-excluded}

- Lenses attached through broad system adapters such as FTZ
- Lenses that can be attached only through a generic mount adapter such as an M42 adapter, or through a third-party adapter
- Products that use a separately sold Z-mount adapter not dedicated to the lens or product series

Products that differ only in color or package contents are not recorded separately unless the manufacturer or brand treats them as separate products.

## Mount adapters {#adapter-dataset}

### Included {#adapter-included}

Products whose primary purpose is adapting another interchangeable-lens mount to the Nikon Z mount are included in a dataset separate from lenses and related optical products.

Use one record for the same marketed product; put selectable mount configurations and other officially named options in variants.
The initial scope covers basic product information, mount combinations, electronic functions, optics, mechanisms, and physical characteristics such as dimensions and weight.
It does not include large compatibility matrices for combinations of lenses, cameras, and firmware.

### Excluded {#adapter-excluded}

Products whose mount conversion role is only incidental are excluded.
Examples include:

- Extension tubes
- Filter adapters
- Focal reducers without mount conversion

## Sources {#sources}

Official product pages, specifications, manuals, and similar sources from the manufacturer or brand are preferred for inclusion decisions and product information.

When an official product page for the exact product is unavailable, a crowdfunding page operated by the manufacturer, corporate investor-relations material or a press release, or a product or announcement page from an authorized distributor may be used as evidence.
An authorized retailer's product page may corroborate that a Z-mount version was released or confirm a manufacturer-published model number.
It is not treated as an official product page.

Do not infer information that cannot be confirmed by a source accepted under these rules.
When sources conflict, do not choose one without supporting evidence.

## Related pages

- [Glossary](glossary.md)
- [Data model](data-model.md)
- [Value-state rules](value-rules.md)
- [Research results](research.md)
